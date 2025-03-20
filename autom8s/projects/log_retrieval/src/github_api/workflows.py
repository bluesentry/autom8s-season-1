import logging
from dataclasses import dataclass

# Authentication is defined via github.Auth
from github import Auth, Github

logger = logging.getLogger(__name__)


@dataclass
class GitHubAPIConnection:
    session: str

    @classmethod
    def connect_to_repo(cls, token: str):
        auth = Auth.Token(token)
        session = Github(auth=auth)
        return cls(session)

    def __enter__(self):
        yield self

    def __exit__(self):
        self.session.close()
