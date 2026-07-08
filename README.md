# ptree

A simple directory tree viewer for your terminal.

```
./
│
├── ptree/
│   ├── __init__.py
│   ├── cli.py
│   └── ptree.py
│
├── .gitignore
├── README.md
└── tree.py
```

## Usage

```
ptree [ROOT] [-d] [-e] [-c] [-o FILE]
```

| Argument | Description |
|---|---|
| `ROOT` | Directory to visualize. Defaults to `.`. |
| `-d`, `--dir-only` | Show directories only, skip files. |
| `-e`, `--emojis` | Decorate items with emoji icons. |
| `-c`, `--color` | Highlight directories in yellow and files in cyan. |
| `-o`, `--output FILE` | Write the tree to a file instead of stdout. |

### Examples

```bash
ptree                           # show current directory
ptree /some/path                # show a specific directory
ptree -d                        # show directories only
ptree -e                        # show with emoji icons
ptree -c                        # show with colored output
ptree -e -o tree.md             # save emoji tree to a file
ptree -c -e                     # emoji + colors together
```

When writing to a file, the tree is wrapped in a fenced code block so it renders nicely in Markdown.
