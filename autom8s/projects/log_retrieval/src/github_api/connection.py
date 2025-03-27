import logging
from dataclasses import dataclass, field
from functools import cached_property

import requests

# Authentication is defined via github.Auth
from github import Auth, AuthenticatedUser, Github, Repository
from github.Workflow import Workflow as GitHubWorkflow
from pydantic import BaseModel

from src.github_api.repository import Repository

logger = logging.getLogger(__name__)


def ensure_token(token: str | None) -> str:
    """Ensure a token is provided.

    Args:
        token (str | None): If `None`, the token will be drawn from secret storage.

    Returns:
        str: The token.

    Raises:
        ValueError: If no token is provided. (fix by integrating secret storage)
    """
    if token:
        return token
    # TODO: draw from secret storage if no token is provided
    raise ValueError("No token provided")


class RetrievalConfig(BaseModel):
    """Model for retrieval based JSON payloads"""

    repos: list[str]


@dataclass
class GitHubAPIConnection:
    """A context manager for connecting to the GitHub API.

    Usage:
        with GitHubAPIConnection.from_token(token) as api:
            api.get_repo(...)
            # Use the GitHub API session here
            pass
    """

    _token: str
    _session: str
    _cached_repos: dict[str, Repository] = field(default_factory=dict)

    @classmethod
    def from_token(cls, token: str):
        auth = Auth.Token(token)
        _session = Github(auth=auth)
        return cls(token, _session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the GitHub API _session."""
        self._session.close()

    @cached_property
    def headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authentication": f"Bearer {self._session.requester.auth.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
x
    @cached_property
    def user(self) -> AuthenticatedUser:
        return self._session.get_user()

    @property
    def repos(self) -> dict[str, Repository]:
        """Cached retrieval of all user repositories"""
        for repo in self.user.get_repos():
            if repo.name not in self._cached_repos:
                self._cached_repos[repo.name] = Repository(repo)

        return self._cached_repos

    def get_repo(self, repo_name: str) -> Repository:
        """Return a repository by name, or None if not found."""
        if cached_repo := self._cached_repos.get(repo_name):
            return cached_repo
        result = self.repos.get(repo_name)
        self._cached_repos[repo_name] = result
        return result

    def get_repos(self, repo_names: list[str]) -> list[Repository]:
        """Return a dictionary of repositories by name, or None if not found."""

        return {name: self.repos.get(name) for name in repo_names}

    def get_workflow_logs(self, workflow: GitHubWorkflow):
        result = requests.get(
            f"{workflow.url}/logs", headers=self.headers, params={"output": "file.zip"}
        )
        breakpoint()
        return result
