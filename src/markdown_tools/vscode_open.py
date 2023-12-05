from pathlib import Path


def vscode_open(ps1_file: Path, file_to_open: Path) -> None:
    """
    Append a file path to a PowerShell script, or create the script if it doesn't exist.

    :param ps1_file: The name of the PowerShell script.
    :param file_to_open: The name of the new file to be added to the script.
    """
    if ps1_file.exists():
        # Read the existing PowerShell script
        lines = ps1_file.read_text().splitlines(True)
    else:
        # Create a new script with the basic structure
        lines = [
            "# PowerShell script to open a list of files in VS Code",
            "",
        ]

    # Identify the line where file paths are assigned or start a new list
    last_file_line = next(
        (
            i
            for i, line in enumerate(lines)
            if line.startswith("$file")
        ),
        -1,  # Return this value if generator expression produces nothing
    )
    new_file_var = f"$file{last_file_line + 2}"  # Incrementing for the new variable
    lines.append(f'{new_file_var} = "{file_to_open.as_posix()}"')

    # Add or update the code command
    code_line = next(
        (
            i
            for i, line in enumerate(lines)
            if line.strip().startswith("code")
        ),
        -1,
    )
    if code_line == -1:
        # Add a new code command if it doesn't exist
        lines.append(f"code {new_file_var}")
    else:
        # Update the existing code command
        lines[code_line] = (
            lines[code_line].rstrip() + f" {new_file_var}"
        )

    # Write the updated script back to the file
    ps1_file.write_text("\n".join(lines))


# Example usage
vscode_open(Path("test.ps1"), Path("file_a.txt"))
vscode_open(Path("test.ps1"), Path("file_b.txt"))
