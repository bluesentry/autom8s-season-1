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
        """Retrieve a workflow by its ID"""
        return self.workflows.get(workflow_id)

    @cached_property
    def workflows(self) -> list[GitHubWorkflow]:
        """Map all workflows to their name for easy retrieval"""
        return {
            workflow.id: workflow for workflow in self._git_repo.get_workflow_runs()
        }

    def all_jobs(self, workflow: GitHubWorkflow):
        """Retrieve all jobs in the given workflow"""
        return [job for job in workflow.get_jobs()]
