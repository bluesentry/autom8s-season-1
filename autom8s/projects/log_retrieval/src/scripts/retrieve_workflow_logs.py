import argparse

from src.lumber import set_log_level


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Retrieve Workflow Logs", usage="%(prog)s [options]"
    )
    parser.add_argument(
        "--repo", required=True, nargs="+", help="GitHub repository URL"
    )
    # if token is not provided, uses a default token from secret storage
    parser.add_argument("--token", required=False, help="GitHub access token")
    return parser


def main(args: argparse.Namespace):
    set_log_level()


if __name__ == "__main__":
    """Get command line arguments and run the main function."""
    parser = get_parser()
    args = parser.parse_args()
    main(args)
