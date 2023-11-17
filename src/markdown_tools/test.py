import typer

app = typer.Typer()


@app.command()
def create():
    print(f"Running create()")


@app.command()
def delete():
    print(f"Running delete()")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print(typer.main.get_command(app).get_help(ctx))
        raise typer.Exit()


if __name__ == "__main__":
    app()
