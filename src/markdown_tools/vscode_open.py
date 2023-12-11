# vscode_open.py
from pathlib import Path


def vscode_open(opener_ps1: Path, file_to_open: Path) -> None:
    # print(f"{opener_ps1.as_posix() = }, {file_to_open = }")
    if opener_ps1.exists():
        lines = opener_ps1.read_text().splitlines()
    else:
        lines = [
            "# PowerShell script to open a list of files in VS Code",
            "",
        ]

    # Find the highest file variable number
    file_vars = [
        line.split("=")[0].strip()
        for line in lines
        if line.startswith("$file")
    ]
    max_file_var_number = max(
        (
            int(var[5:])
            for var in file_vars
            if var.startswith("$file") and var[5:].isdigit()
        ),
        default=0,
    )

    # Add the new file variable
    new_file_var = f"$file{max_file_var_number + 1}"
    lines.append(f'{new_file_var} = "{file_to_open.as_posix()}"')

    # Update or add the code command at the end
    # Remove the existing code line if it exists
    lines = [
        line for line in lines if not line.strip().startswith("code")
    ]

    # Reconstruct the code line with all file variables
    file_vars = [
        line.split("=")[0].strip()
        for line in lines
        if line.startswith("$file")
    ]
    code_line = "code " + " ".join(file_vars)
    lines.append(code_line)

    # Write the updated script back to the file
    opener_ps1.write_text("\n".join(lines) + "\n")
    # print(opener_ps1.read_text())


if __name__ == "__main__":  # Example usage
    test_ps1 = Path("test.ps1")
    if test_ps1.exists():
        test_ps1.unlink()
    vscode_open(test_ps1, Path("file_a.txt"))
    vscode_open(test_ps1, Path("file_b.txt"))
    vscode_open(test_ps1, Path("file_c.txt"))
    vscode_open(test_ps1, Path("file_d.txt"))
    vscode_open(test_ps1, Path("file_e.txt"))
