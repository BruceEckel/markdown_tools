# Markdown Tools
For working with markdown chapters in a programming book.

To install:

1. [Install Python](https://www.python.org/about/gettingstarted/) if you don't already have it.

1. Clone this repository. 

1. Open a command prompt and change to this project directory. Run this command:

```text
pip install -e .
```

This performs a system-wide install from the current directory '.', and the
`-e` flag makes it editable, which means that if you make any changes to the
tools, those changes are immediately available without re-running `pip`. 
(If you're not planning to modify the tools you can leave off the `-e`).

After installation, all consoles will contain the command `mt` which is an
entry point to all the markdown tools. If you would like a different command name,
open `pyproject.toml` and find this section:

```text
[project.scripts]
mt = "markdown_tools.tools:main"
```

Then change `mt` to the command of your choice. 
(In this case, you will need to re-run `pip` to change the name).
