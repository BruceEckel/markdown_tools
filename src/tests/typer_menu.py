from typing import Optional
import typer
from typing_extensions import Annotated

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h"]},
)


def menu_callback(value: bool):
    if value:
        print("Inside menu_callback")
        raise typer.Exit()


def main(
    value: Annotated[
        Optional[bool],
        typer.Option("-m", callback=menu_callback),
    ] = None,
):
    print("Hello")


if __name__ == "__main__":
    typer.run(main)
