"""
ptree CLI.
"""

import argparse
import pathlib
import sys

from . import __version__
from .ptree import DirectoryTree


def main() -> None:
    args = parse_cmd_line_arguments()
    root = pathlib.Path(args.root)

    if not root.is_dir():
        print(f"Error: {root} is not a directory.")
        sys.exit(1)

    tree = DirectoryTree(root)
    tree.generate()


def parse_cmd_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ptree",
        description="ptree - a simple directory tree viewer",
        epilog="Thanks for using ptree!",
    )

    parser.version = f"ptree {__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "root",
        metavar="ROOT",
        nargs="?",
        default=".",
        help="the root directory to start the tree from",
    )

    return parser.parse_args()
