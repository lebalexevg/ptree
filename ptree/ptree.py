"""
ptree - a simple directory tree viewer
"""

import os
import pathlib

PIPE = "|"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root) -> None:
        self._generator = _TreeGenerator(root)

    def generate(self):
        tree = self._generator.build()

        for entry in tree:
            print(entry)


class _TreeGenerator:
    def __init__(self, root) -> None:
        self._root = pathlib.Path(root)
        self._tree = []

    def build(self) -> list[str]:
        self._tree_head()
        self._tree_body(self._root)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory: pathlib.Path, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE

            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(
        self,
        directory: pathlib.Path,
        index: int,
        entries_count: int,
        prefix: str,
        connector: str,
    ) -> None:
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")

        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX

        self._tree_body(directory, prefix)

        self._tree.append(prefix.rstrip())

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str) -> None:
        self._tree.append(f"{prefix}{connector} {file.name}")
