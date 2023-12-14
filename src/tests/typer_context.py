import typer

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
    rich_markup_mode="rich",
)


@app.command("1")
def create(username: str):
    "Create user"
    print(f"Creating user: {username}")


@app.command("2")
def delete(username: str):
    "Delete user"
    print(f"Deleting user: {username}")


@app.callback()
def main(ctx: typer.Context):
    """
    Manage users in the awesome CLI app.
    """
    print(f"About to execute command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
