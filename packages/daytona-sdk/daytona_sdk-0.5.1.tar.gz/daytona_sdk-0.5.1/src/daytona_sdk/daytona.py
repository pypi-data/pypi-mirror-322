"""
Daytona SDK for Python

This module provides the main entry point for interacting with Daytona Server API.
"""

import os
import uuid
import json
from typing import Optional, Literal, Dict, Any
from dataclasses import dataclass
from environs import Env
import time

from .code_toolbox.workspace_python_code_toolbox import WorkspacePythonCodeToolbox
from .code_toolbox.workspace_ts_code_toolbox import WorkspaceTsCodeToolbox
from .workspace import Workspace
from api_client import (
    Configuration,
    WorkspaceApi,
    GitProviderApi,
    WorkspaceToolboxApi,
    ApiClient,
)

# Type definitions
CodeLanguage = Literal["python", "javascript", "typescript"]


@dataclass
class DaytonaConfig:
    """Configuration options for initializing the Daytona client.
    
    Args:
        api_key: API key for authentication with Daytona server
        server_url: URL of the Daytona server
        target: Target environment for workspaces
    """
    api_key: str
    server_url: str
    target: str


@dataclass
class CreateWorkspaceParams:
    """Parameters for creating a new workspace.
    
    Args:
        id: Optional workspace ID. If not provided, a random ID will be generated
        image: Optional Docker image to use for the workspace
        language: Programming language to use in the workspace
        os_user: Optional OS user for the workspace image
    """
    language: CodeLanguage
    id: Optional[str] = None
    image: Optional[str] = None
    os_user: Optional[str] = None
    env_vars: Optional[Dict[str, str]] = None
    # labels: Optional[Dict[str, str]] = None


class Daytona:
    def __init__(self, config: Optional[DaytonaConfig] = None):
        """
        Initialize Daytona instance with optional configuration.
        If no config is provided, reads from environment variables using environs.

        Args:
            config: Optional DaytonaConfig object containing api_key, server_url, and target

        Raises:
            ValueError: If API key or Server URL is not provided either through config or environment variables
        """
        if config is None:
            # Initialize env - it automatically reads from .env and .env.local
            env = Env()
            env.read_env()  # reads .env
            # reads .env.local and overrides values
            env.read_env(".env.local", override=True)

            self.api_key = env.str("DAYTONA_API_KEY")
            self.server_url = env.str("DAYTONA_SERVER_URL")
            self.target = env.str("DAYTONA_TARGET", "local")
        else:
            self.api_key = config.api_key
            self.server_url = config.server_url
            self.target = config.target

        if not self.api_key:
            raise ValueError("API key is required")

        if not self.server_url:
            raise ValueError("Server URL is required")

        # Create API configuration without api_key
        configuration = Configuration(host=self.server_url)
        api_client = ApiClient(configuration)
        api_client.default_headers["Authorization"] = f"Bearer {self.api_key}"

        # Initialize API clients with the api_client instance
        self.git_provider_api = GitProviderApi(api_client)
        self.workspace_api = WorkspaceApi(api_client)
        self.toolbox_api = WorkspaceToolboxApi(api_client)

    def create(self, params: Optional[CreateWorkspaceParams] = None) -> Workspace:
        """Creates a new workspace and waits for it to start.
        
        Args:
            params: Optional parameters for workspace creation. If not provided, 
                   defaults to Python language.
            
        Returns:
            The created workspace instance
        """
        if params.id:
            workspace_id = params.id
        else:
            workspace_id = f"sandbox-{str(uuid.uuid4())[:8]}"

        code_toolbox = self._get_code_toolbox(params)

        try:
            # Create project as a dictionary
            project = {
                "name": "main",
                "image": (
                    params.image if params and params.image 
                    else code_toolbox.get_default_image()
                ),
                "osUser": (
                    params.os_user if params and params.os_user
                    else "daytona" if code_toolbox.get_default_image() 
                    else "root"
                ),
                "env_vars": params.env_vars if params and params.env_vars else {},
                "source": {
                    "repository": {
                        "branch": "main",
                        "clone_target": "branch",
                        "id": "python-helloworld",
                        "name": "python-helloworld",
                        "owner": "dbarnett",
                        "path": None,
                        "pr_number": None,
                        "sha": "288d7ced1b971fd1b3b0c36002b96e1c3f91542e",
                        "source": "github.com",
                        "url": "https://github.com/dbarnett/python-helloworld.git",
                    }
                },
            }

            # Create workspace using dictionary
            workspace_data = {
                "id": workspace_id,
                "name": workspace_id,
                "projects": [project],
                "target": self.target,
            }

            response = self.workspace_api.create_workspace(workspace=workspace_data)
            workspace = Workspace(workspace_id, response, self.toolbox_api, code_toolbox)

            # Wait for workspace to start
            try:
                if not workspace.instance.projects[0].info.provider_metadata:
                    raise Exception("Provider metadata is missing")
                
                provider_metadata = json.loads(workspace.instance.projects[0].info.provider_metadata)
                current_state = provider_metadata.get('state')
                while current_state in ["unknown", "pulling_image", "creating"]:
                    time.sleep(0.1)
                    workspace_check = self.workspace_api.get_workspace(workspace_id=workspace.id)
                    if not workspace_check.projects[0].info.provider_metadata:
                        raise Exception("Provider metadata is missing during status check")
                    provider_metadata = json.loads(workspace_check.projects[0].info.provider_metadata)
                    current_state = provider_metadata.get('state')
                    
                if current_state != "started":
                    raise Exception(f"Workspace failed to start. Current state: {current_state}")
            finally:
                # If not Daytona SaaS, we don't need to handle pulling image state
                pass

            return workspace

        except Exception as e:
            try:
                self.workspace_api.remove_workspace(workspace_id=workspace_id)
            except:
                pass
            raise Exception(f"Failed to create workspace: {str(e)}") from e

    def _get_code_toolbox(self, params: Optional[CreateWorkspaceParams] = None):
        """Helper method to get the appropriate code toolbox
        
        Args:
            params: Optional workspace parameters. If not provided, defaults to Python toolbox.
            
        Returns:
            The appropriate code toolbox instance
        """
        if not params:
            return WorkspacePythonCodeToolbox()

        match params.language:
            case "javascript" | "typescript":
                return WorkspaceTsCodeToolbox()
            case "python":
                return WorkspacePythonCodeToolbox()
            case _:
                raise ValueError(f"Unsupported language: {params.language}")

    def remove(self, workspace: Workspace) -> None:
        """Removes a workspace.
        
        Args:
            workspace: The workspace to remove
        """
        return self.workspace_api.remove_workspace(workspace_id=workspace.id)

    def get_current_workspace(self, workspace_id: str) -> Workspace:
        """
        Get a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace to retrieve

        Returns:
            Workspace: The workspace instance

        Raises:
            ValueError: If workspace_id is not provided
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")

        # Get the workspace instance
        workspace_instance = self.workspace_api.get_workspace(workspace_id=workspace_id)

        # Create and return workspace with Python code toolbox as default
        code_toolbox = WorkspacePythonCodeToolbox()
        return Workspace(
            workspace_id, workspace_instance, self.toolbox_api, code_toolbox
        )
