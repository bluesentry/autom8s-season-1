import logging
from dataclasses import dataclass

# Authentication is defined via github.Auth
from github import Auth, Github

logger = logging.getLogger(__name__)


@dataclass
class GitHubAPIConnection:
    """A context manager for connecting to the GitHub API.

    Usage:
        with GitHubAPIConnection.from_token(token) as api:
            api.get_repo(...)
            # Use the GitHub API session here
            pass
    """

    session: str

    @classmethod
    def from_toekn(cls, token: str):
        auth = Auth.Token(token)
        session = Github(auth=auth)
        return cls(session)

    def __enter__(self):
        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the GitHub API session."""
        self.session.close()

    def get_repo(self, url: str):
        return self.session.get_repo(url)
