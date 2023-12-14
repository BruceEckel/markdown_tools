import typer
from typing_extensions import Annotated

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
    rich_markup_mode="rich",
)


# @app.callback()
def name_callback(value: str):
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


# @app.callback()
# def foo():
#     print("FOO!")


@app.command("1")
def main(name: Annotated[str, typer.Option(callback=name_callback)]):
    print(f"Hello {name}")


if __name__ == "__main__":
    # typer.run(main)
    app()
