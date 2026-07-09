"""
ptree - a simple directory tree viewer
"""

import os
import pathlib
import sys

from typing import TypedDict

PIPE = "|"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

OPEN_DIRECTORY_ICON = "📁"
CLOSED_DIRECTORY_ICON = "📂"
FILE_ICON = "📄"

ROOT_COLOR_CODE = "\x1b[32m"
DIRECTORY_COLOR_CODE = "\x1b[33m"
FILE_COLOR_CODE = "\x1b[36m"
BOLD_FONT_CODE = "\x1b[1m"
RESET_CODE = "\x1b[0m"


class Statistics(TypedDict):
    directories: int
    files: int
    total: int


class DirectoryTree:
    def __init__(
        self,
        root: pathlib.Path,
        dir_only: bool = False,
        show_emojis: bool = False,
        use_color: bool = False,
        show_hidden: bool = False,
        show_stats: bool = True,
        output=sys.stdout,
    ) -> None:
        self._output = output
        self._generator = _TreeGenerator(
            root, dir_only, show_emojis, show_hidden, use_color,
        )
        self._show_stats = show_stats

    def generate(self):
        tree = self._generator.build()

        if self._output != sys.stdout:
            tree.insert(0, "```")
            tree.append("```")

            if isinstance(self._output, (str, pathlib.Path)):
                self._output = open(self._output, mode="w", encoding="utf-8")
            else:
                raise TypeError(
                    f"output must be a file path, got {type(self._output)} instead"
                )

        stats = self._generator.get_stats()

        with self._output as stream:
            for entry in tree:
                print(entry, file=stream)

            if self._show_stats:
                statistics = (
                    "\n"
                    f"{BOLD_FONT_CODE}Total:{RESET_CODE} {stats['total']} \n"
                    f"{BOLD_FONT_CODE}Directories:{RESET_CODE} {stats['directories']} \n"
                    f"{BOLD_FONT_CODE}Files:{RESET_CODE} {stats['files']}"
                )

                print(statistics, file=stream)


class _TreeGenerator:
    def __init__(
        self,
        root: pathlib.Path,
        dir_only: bool = False,
        show_emojis: bool = False,
        show_hidden: bool = False,
        use_color: bool = False,
    ) -> None:
        self._root = root
        self._dir_only = dir_only
        self._show_emojis = show_emojis
        self._show_hidden = show_hidden
        self._use_color = use_color
        self._tree = []
        self._stats: Statistics = {"directories": 0, "files": 0, "total": 0}

    def build(self) -> list[str]:
        self._tree_head()
        self._tree_body(self._root)
        return self._tree

    def get_stats(self) -> Statistics:
        return self._stats

    def _tree_head(self) -> None:
        self._tree.append(
            f"{BOLD_FONT_CODE}{ROOT_COLOR_CODE}{self._root}{os.sep}{RESET_CODE}"
        )
        self._tree.append(PIPE)

    def _tree_body(self, directory: pathlib.Path, prefix=""):
        entries = self._prepare_entries(directory)
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE

            if entry.is_dir():
                self._stats["directories"] += 1
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._stats["files"] += 1
                self._add_file(entry, prefix, connector)

            self._stats["total"] += 1

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        entries = directory.iterdir()

        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]

        if not self._show_hidden:
            entries = [entry for entry in entries if not entry.name.startswith(".")]

        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    def _add_directory(
        self,
        directory: pathlib.Path,
        index: int,
        entries_count: int,
        prefix: str,
        connector: str,
    ) -> None:

        emoji = (
            f" {CLOSED_DIRECTORY_ICON if any(directory.iterdir()) else OPEN_DIRECTORY_ICON}"
            if self._show_emojis
            else ""
        )

        body = f"{BOLD_FONT_CODE}{DIRECTORY_COLOR_CODE if self._use_color else ''}{emoji} {directory.name}{os.sep}{RESET_CODE}"

        self._tree.append(f"{prefix}{connector}{body}")

        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX

        self._tree_body(directory, prefix)

        self._tree.append(prefix.rstrip())

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str) -> None:
        emoji = f" {FILE_ICON}" if self._show_emojis else ""
        body = f"{FILE_COLOR_CODE if self._use_color else ''}{emoji} {file.name}{RESET_CODE if self._use_color else ''}"

        self._tree.append(f"{prefix}{connector}{body}")
