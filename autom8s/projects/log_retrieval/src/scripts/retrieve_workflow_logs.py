import argparse
import json

from src.github_api.connection import GitHubAPIConnection, RetrievalConfig, ensure_token
from src.lumber import set_log_level


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Retrieve Workflow Logs", usage="%(prog)s [options]"
    )
    parser.add_argument(
        "--payload-file",
        required=True,
        help="Example payload for retrieving workflow logs",
    )
    # if token is not provided, uses a default token from secret storage
    parser.add_argument("--token", required=False, help="GitHub access token")
    return parser


def main(args: argparse.Namespace):
    set_log_level()
    token = ensure_token(args.token)
    with open(args.payload_file) as payload_file:
        payload = json.load(payload_file)

    retrieval_config = RetrievalConfig.model_validate(payload)
    with GitHubAPIConnection.from_token(token) as api:
        repos = api.get_repos(retrieval_config.repos)
        repo = repos.get("ai_ml_competition_2025_0")
        workflow = repo.get_workflow(13707342501)
        logs = api.get_workflow_logs(workflow)
        breakpoint()


if __name__ == "__main__":
    """Get command line arguments and run the main function.

    This is a sample entrypoint. More than likely, the "Get git workflow logs" logic
    will be triggered by an API call.
    """
    parser = get_parser()
    args = parser.parse_args()
    main(args)
