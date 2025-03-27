from dataclasses import dataclass
from functools import cached_property

from github.Repository import Repository as GitHubRepository
from github.Workflow import Workflow as GitHubWorkflow


@dataclass
class Repository:
    """AutoM8s interpretation of a GitHub repository"""

    _git_repo: GitHubRepository

    def __post_init__(self):
        """Establish an empty workflow cache"""
        self._cached_workflows: dict[int, GitHubWorkflow] = {}

    def get_workflow(self, workflow_id: int) -> GitHubWorkflow | None:
        return self.workflows.get(workflow_id)

    @cached_property
    def workflows(self) -> list[GitHubWorkflow]:
        return {
            workflow.id: workflow for workflow in self._git_repo.get_workflow_runs()
        }

    def all_jobs(self, workflow: GitHubWorkflow):
        return [job for job in workflow.get_jobs()]
