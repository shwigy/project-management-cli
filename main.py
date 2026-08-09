"""CLI entry point for the project management tool."""

from src.cli.parser import build_parser
from src.utils.storage import load_data


def main():
    load_data()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
