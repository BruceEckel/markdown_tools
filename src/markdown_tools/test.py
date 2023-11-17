import typer

app = typer.Typer()


@app.command()
def create(username: str):
    print(f"Creating user: {username}")


@app.command()
def delete(username: str):
    print(f"Deleting user: {username}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print("running without a subcommand")
        print(typer.main.get_command(app).get_help(ctx))
        raise typer.Exit()


if __name__ == "__main__":
    app()
