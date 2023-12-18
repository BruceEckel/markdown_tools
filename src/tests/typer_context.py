import typer
import readchar  # Reads a single character, no CR required

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
    rich_markup_mode="rich",
    epilog="Shows up after the help message",
)


@app.command("1")
def one():
    "Command One"
    print("This is Command One!")


@app.command("2")
def two():
    "Command Two"
    print("This is Command Two!")


@app.command("m")
def menu(ctx: typer.Context):
    "Menu Mode"
    print("This is Menu Mode!")


@app.callback()
def main(ctx: typer.Context):
    """
    Attempt to create a menu-driven Typer app
    """
    if ctx.invoked_subcommand == "m":
        print(ctx.get_help())
        while (key := readchar.readchar()) not in "12":
            print(key)
        print(f"You selected {key}")
        match key:
            case "1":
                ctx.call_on_close(one)
            case "2":
                ctx.call_on_close(two)


if __name__ == "__main__":
    app()
