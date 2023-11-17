# Markdown Tools
For working with markdown chapters in a programming book.

To install:

1. Download and unpack this repository. 

2. Move to this project directory and enter:

```text
> pip install -e .
```

This performs a system-wide install from the current directory '.', and the
`-e` flag makes it editable, which means that if you make any changes to the
tools, those changes are immediately available without re-running `pip`.

After the installation, any console will contain the command `mt` which is an
entry point to all the markdown tools. If you would like a different command name,
open `pyproject.toml` and find this section:

```text
[project.scripts]
mt = "markdown_tools.tools:main"
```

Then change `mt` to the command of your choice. 
(In this case, you *will* need to re-run `pip` to change the name).
