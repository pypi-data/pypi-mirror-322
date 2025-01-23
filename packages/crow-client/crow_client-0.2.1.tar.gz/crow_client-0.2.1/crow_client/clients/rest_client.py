import ast
import base64
import importlib.metadata
import inspect
import json
import logging
import os
from pathlib import Path
from types import ModuleType
from typing import Any, ClassVar
from uuid import UUID

import cloudpickle
import google.auth.transport.requests
import httpx
from aviary.functional import EnvironmentBuilder
from google.auth import default
from google.oauth2 import service_account
from httpx import HTTPStatusError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

from crow_client.models.app import (
    CrowDeploymentConfig,
    Stage,
)
from crow_client.utils.module_utils import (
    OrganizationSelector,
    fetch_environment_function_docstring,
)

logger = logging.getLogger(__name__)


FILE_UPLOAD_IGNORE_PARTS = {
    ".ruff_cache",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
}


class RestClientError(Exception):
    """Base exception for REST client errors."""


class JobFetchError(RestClientError):
    """Raised when there's an error fetching a job."""


class JobCreationError(RestClientError):
    """Raised when there's an error creating a job."""


class InvalidTaskDescriptionError(Exception):
    """Raised when the task description is invalid or empty."""


class RestClient:
    REQUEST_TIMEOUT: ClassVar[float] = 30.0  # sec
    MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
    RETRY_MULTIPLIER: ClassVar[int] = 1
    MAX_RETRY_WAIT: ClassVar[int] = 10

    def __init__(self, stage: Stage = Stage.DEV, organization: str | None = None):
        self.base_url = stage.value
        self.auth_jwt = self._run_auth()
        self.organizations: list[str] = self._filter_orgs(organization)

    def _filter_orgs(self, organization: str | None = None) -> list[str]:
        filtered_orgs = [
            org
            for org in self._fetch_my_orgs()
            if (org == organization or organization is None)
        ]
        if not filtered_orgs:
            raise ValueError(f"Organization '{organization}' not found.")
        return filtered_orgs

    def _run_auth(self) -> str:
        # Service accounts cannot route through the same auth flow as user accounts
        # this path is almost exclusively used by CI
        service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
        if service_account_json is not None:
            service_account_info = json.loads(service_account_json)
            credentials = service_account.IDTokenCredentials.from_service_account_info(
                service_account_info,
                target_audience=self.base_url,
            )

            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            return credentials.token

        credentials, _ = default()
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        return credentials.id_token

    def _check_job(self, name: str, organization: str) -> dict[str, Any]:
        try:
            with self.get_client() as client:
                response = client.get(
                    f"/v0.1/check-crow/crow/{name}/organization/{organization}",
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise JobFetchError(f"Error checking job: {e!s}") from e

    def _fetch_my_orgs(self) -> list[str]:
        with self.get_client() as client:
            response = client.get("/v0.1/my-organizations")
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _validate_module_path(path: Path) -> None:
        """Validates that the given path exists and is a directory.

        Args:
            path: Path to validate

        Raises:
            JobFetchError: If the path is not a directory

        """
        if not path.is_dir():
            raise JobFetchError(f"Path {path} is not a directory")

    @staticmethod
    def _validate_template_path(template_path: str | os.PathLike) -> None:
        """
        Validates that a template path exists and is a file.

        Args:
            template_path: Path to validate

        Raises:
            FileNotFoundError: If the template path doesn't exist
            ValueError: If the path exists but isn't a file
        """
        template_path = Path(template_path)
        if not template_path.exists():
            raise FileNotFoundError(
                f"Markdown template file not found: {template_path}"
            )
        if not template_path.is_file():
            raise ValueError(
                f"Markdown template path exists but is not a file: {template_path}"
            )

    @staticmethod
    def _validate_files(files: list, path: str | os.PathLike) -> None:
        """Validates that files were found in the given path.

        Args:
            files: List of collected files
            path: Path that was searched for files

        Raises:
            JobFetchError: If no files were found

        """
        if not files:
            raise JobFetchError(f"No files found in {path}")

    def get_client(self, content_type: str | None = "application/json") -> httpx.Client:
        """Get HTTP client with Google credentials from ADC.

        Args:
            content_type: Optional content type header. Set to None for multipart uploads.

        """
        headers = {"Authorization": f"Bearer {self.auth_jwt}"}
        if content_type:
            headers["Content-Type"] = content_type

        return httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.REQUEST_TIMEOUT,
        )

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    )
    def get_job(self, job_id: str | None = None, history: bool = False):
        """Get details for a specific crow job."""
        try:
            job_id = job_id or self.trajectory_id
            with self.get_client() as client:
                response = client.get(
                    f"/v0.1/crow-jobs/{job_id}",
                    params={"history": history},
                )
                response.raise_for_status()
                return response.json()
        except ValueError as e:
            raise ValueError("Invalid job ID format. Must be a valid UUID.") from e
        except Exception as e:
            raise JobFetchError(f"Error getting job: {e!s}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    )
    def create_job(self, data: dict):
        """Create a new crow job."""
        try:
            with self.get_client() as client:
                response = client.post("/v0.1/crow-jobs", json=data)
                response.raise_for_status()
                self.trajectory_id = response.json()
                return self.trajectory_id
        except Exception as e:
            raise JobFetchError(f"Error getting job: {e!s}") from e

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    )
    def get_build_status(self, build_id: UUID | None = None) -> dict[str, Any]:
        """Get the status of a build."""
        with self.get_client() as client:
            build_id = build_id or self.build_id
            response = client.get(f"/v0.1/build-crow/{build_id}")
            response.raise_for_status()
            return response.json()

    # TODO: Refactor later so we don't have to ignore PLR0915
    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
    )
    def create_crow(  # noqa: PLR0915
        self,
        config: CrowDeploymentConfig,
    ) -> dict[str, Any]:
        """Creates a crow deployment from the environment and environment files.

        Args:
            config: Configuration object containing all necessary parameters for crow deployment.

        Returns:
            A response object containing metadata of the build.

        """
        task_description: str = config.task_description or str(
            fetch_environment_function_docstring(
                config.environment,
                config.path,  # type: ignore[arg-type]
                "from_task",
            )
            if config.functional_environment is None
            else config.functional_environment.start_fn.__doc__
        )
        if not task_description or not task_description.strip():
            raise InvalidTaskDescriptionError(
                "Task description cannot be None or empty. Ensure your from_task environment function has a valid docstring."
                " If you are deploying with your Environment as a dependency, "
                "you must add a `task_description` to your `CrowDeploymentConfig`.",
            )
        selected_org = OrganizationSelector.select_organization(self.organizations)
        if selected_org is None:
            return {
                "status": "cancelled",
                "message": "Organization selection cancelled",
            }

        try:
            module_name = (
                Path(config.path).name
                if config.path
                else config.functional_environment.__name__  # type: ignore[union-attr]
            )

            try:
                job_status = self._check_job(module_name, selected_org)
                if job_status["exists"]:
                    if config.force:
                        logger.warning(
                            f"Overwriting existing deployment '{job_status['name']}",
                        )
                    else:
                        user_response = input(
                            f"A deployment named '{module_name}' already exists. Do you want to proceed? [y/N]: ",
                        )
                        if user_response.lower() != "y":
                            logger.info("Deployment cancelled.")
                            return {
                                "status": "cancelled",
                                "message": "User cancelled deployment",
                            }
            except Exception:
                logger.warning("Unable to check for existing deployment, proceeding.")

            encoded_pickle = None
            if config.functional_environment is not None:
                # TODO(remo): change aviary fenv code to have this happen automatically.
                for t in config.functional_environment.tools:
                    t._force_pickle_fn = True
                pickled_env = cloudpickle.dumps(config.functional_environment)
                encoded_pickle = base64.b64encode(pickled_env).decode("utf-8")

            files = []
            for file_path in Path(config.path).rglob("*") if config.path else []:
                if any(
                    ignore in file_path.parts for ignore in FILE_UPLOAD_IGNORE_PARTS
                ):
                    continue

                if file_path.is_file():
                    relative_path = (
                        f"{module_name}/{file_path.relative_to(config.path)}"  # type: ignore[arg-type]
                    )
                    files.append(
                        (
                            "files",
                            (
                                relative_path,
                                file_path.read_bytes(),
                                "application/octet-stream",
                            ),
                        ),
                    )
            if (
                config.functional_environment is not None
                and config.requirements is not None
            ):
                requirements_content = "\n".join(config.requirements)
                files.append(
                    (
                        "files",
                        (
                            f"{config.environment}/requirements.txt",
                            requirements_content.encode(),
                            "text/plain",
                        ),
                    ),
                )

            if config.path:
                self._validate_files(files, config.path)

            markdown_template_file = None
            if config.markdown_template_path:
                self._validate_template_path(config.markdown_template_path)
                template_path = Path(config.markdown_template_path)
                markdown_template_file = (
                    "files",
                    (
                        "markdown_template",
                        template_path.read_bytes(),
                        "application/octet-stream",
                    ),
                )

            logger.debug(f"Sending files: {[f[1][0] for f in files]}")

            data = {
                "agent": config.agent,
                "organization": selected_org,
                "environment": config.environment,
                "functional_environment_pickle": encoded_pickle,
                "python_version": config.python_version,
                "task_description": task_description,
                "environment_variables": json.dumps(config.environment_variables)
                if config.environment_variables
                else None,
                "container_config": config.container_config.model_dump_json()
                if config.container_config
                else None,
                "timeout": config.timeout,
                "storage_dir": config.storage_location,
                "frame_paths": json.dumps(
                    [fp.model_dump() for fp in config.frame_paths],
                )
                if config.frame_paths
                else None,
            }

            with self.get_client(content_type=None) as client:
                response = client.post(
                    "/v0.1/build-crow",
                    data=data,
                    files=[*files, markdown_template_file]
                    if markdown_template_file
                    else files,
                    headers={"Accept": "application/json"},
                    params={"internal-deps": config.requires_aviary_internal},
                )
            try:
                response.raise_for_status()
                build_context = response.json()
                self.build_id = build_context["build_id"]
            except HTTPStatusError as e:
                error_detail = response.json()
                error_message = error_detail.get("detail", str(e))
                raise JobFetchError(f"Server validation error: {error_message}") from e
        except Exception as e:
            raise JobFetchError(f"Error generating docker image: {e!s}") from e
        return build_context


def get_installed_packages() -> dict[str, str]:
    """Returns a dictionary of installed packages and their versions."""
    return {
        dist.metadata["Name"].lower(): dist.version
        for dist in importlib.metadata.distributions()
    }


def get_global_imports(global_scope: dict) -> dict[str, str]:
    """Retrieve global imports from the global scope, mapping aliases to full module names."""
    return {
        name: obj.__name__
        for name, obj in global_scope.items()
        if isinstance(obj, ModuleType)
    }


def get_referenced_globals_from_source(source_code: str) -> set[str]:
    """Extract globally referenced symbols from the source code."""
    parsed = ast.parse(source_code)
    return {
        node.id
        for node in ast.walk(parsed)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def get_used_global_imports(
    func,
    global_imports: dict[str, str],
    global_scope: dict,
    visited=None,
) -> set[str]:
    """Retrieve global imports used by a function."""
    if visited is None:
        visited = set()
    if func in visited:
        return set()
    visited.add(func)

    used_imports: set[str] = set()

    source_code = inspect.getsource(func)
    referenced_globals = get_referenced_globals_from_source(source_code)

    used_imports.update(
        global_imports[name] for name in referenced_globals if name in global_imports
    )

    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            ref_func = global_scope.get(node.func.id)
            if callable(ref_func):
                used_imports.update(
                    get_used_global_imports(
                        ref_func,
                        global_imports,
                        global_scope,
                        visited,
                    ),
                )

    return used_imports


def get_used_modules(env_builder: EnvironmentBuilder, global_scope: dict) -> set[str]:
    """Retrieve globally imported modules referenced by the start_fn and tools."""
    if not isinstance(env_builder, EnvironmentBuilder):
        raise TypeError("The provided object is not an instance of EnvironmentBuilder.")

    global_imports = get_global_imports(global_scope)

    used_imports = get_used_global_imports(
        env_builder.start_fn,
        global_imports,
        global_scope,
    )

    for tool in env_builder.tools:
        used_imports.update(
            get_used_global_imports(tool._tool_fn, global_imports, global_scope),
        )

    return used_imports


def generate_requirements(
    env_builder: EnvironmentBuilder,
    global_scope: dict,
) -> list[str]:
    """Generates a list of modules to install based on loaded modules."""
    used_modules = get_used_modules(env_builder, global_scope)
    used_modules.add("cloudpickle")
    installed_packages = get_installed_packages()

    pip_modules = {module for module in used_modules if module in installed_packages}
    return [f"{module}=={installed_packages[module]}" for module in sorted(pip_modules)]
