import os

from typing import Optional

from ._internal._client._iam_client import IAMClient
from ._internal._manager._artifact_manager import ArtifactManager
from ._internal._manager._task_manager import TaskManager


class Client:
    def __init__(self, client_id: Optional[str] = "", email: Optional[str] = "", password: Optional[str] = ""):
        if not client_id or not client_id.strip():
            client_id = os.getenv("GMI_CLOUD_CLIENT_ID")
        if not email or not email.strip():
            email = os.getenv("GMI_CLOUD_EMAIL")
        if not password or not password.strip():
            password = os.getenv("GMI_CLOUD_PASSWORD")

        if not client_id:
            raise ValueError("Client ID must be provided.")
        if not email:
            raise ValueError("Email must be provided.")
        if not password:
            raise ValueError("Password must be provided.")

        self.iam_client = IAMClient(client_id, email, password)
        self.iam_client.login()

        # Managers are lazily initialized through private attributes
        self._artifact_manager = None
        self._task_manager = None

    @property
    def artifact_manager(self):
        """
        Lazy initialization for ArtifactManager.
        Ensures the Client instance controls its lifecycle.
        """
        if self._artifact_manager is None:
            self._artifact_manager = ArtifactManager(self.iam_client)
        return self._artifact_manager

    @property
    def task_manager(self):
        """
        Lazy initialization for TaskManager.
        Ensures the Client instance controls its lifecycle.
        """
        if self._task_manager is None:
            self._task_manager = TaskManager(self.iam_client)
        return self._task_manager
