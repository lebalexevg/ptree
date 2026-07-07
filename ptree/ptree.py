"""
ptree - a simple directory tree viewer
"""

import os
import pathlib
import sys

PIPE = "|"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

OPEN_DIRECTORY_ICON = "📁"
CLOSED_DIRECTORY_ICON = "📂"
FILE_ICON = "📄"


class DirectoryTree:
    def __init__(
        self,
        root: pathlib.Path,
        dir_only: bool = False,
        show_emojis: bool = False,
        output=sys.stdout,
    ) -> None:
        self._output = output
        self._generator = _TreeGenerator(root, dir_only, show_emojis)

    def generate(self):
        tree = self._generator.build()

        if self._output != sys.stdout:
            tree.insert(0, "```")
            tree.append("```")

            self._output = open(self._output, mode="w", encoding="utf-8")

        with self._output as stream:
            for entry in tree:
                print(entry, file=stream)


class _TreeGenerator:
    def __init__(
        self, root: pathlib.Path, dir_only: bool = False, show_emojis: bool = False
    ) -> None:
        self._root = root
        self._dir_only = dir_only
        self._show_emojis = show_emojis
        self._tree = []

    def build(self) -> list[str]:
        self._tree_head()
        self._tree_body(self._root)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory: pathlib.Path, prefix=""):
        entries = self._prepare_entries(directory)
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE

            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        entries = directory.iterdir()

        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries

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

        print(self._dir_only)

        self._tree.append(f"{prefix}{connector}{emoji} {directory.name}{os.sep}")

        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX

        self._tree_body(directory, prefix)

        self._tree.append(prefix.rstrip())

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str) -> None:
        emoji = f" {FILE_ICON}" if self._show_emojis else ""

        self._tree.append(f"{prefix}{connector}{emoji} {file.name}")
