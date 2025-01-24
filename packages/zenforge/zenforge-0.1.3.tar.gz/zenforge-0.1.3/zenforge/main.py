from typing import Annotated
from pathlib import Path

from zenforge import ProjectType, console
from zenforge.cli import MSG_MAPPER, MessageHandler, CommonErrorCodes
from zenforge.create.method import CreateCommand

import typer

app = typer.Typer(rich_markup_mode="rich", pretty_exceptions_enable=True)

msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command()
def create(
    project_name: Annotated[str, typer.Argument(..., help="The name of the project.")],
    project_type: Annotated[
        ProjectType,
        typer.Argument(..., help="The type of project to create."),
    ] = "basic",
    ci_deps: Annotated[
        bool,
        typer.Option(
            ...,
            help="A flag to include CI dependencies, such as 'git-cliff'.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """
    Creates a new project with [green]PROJECT_NAME[/green] and a [yellow]PROJECT_TYPE[/yellow].

    Project types -
    1) [yellow]BASIC[/yellow]: a simple project with Pydantic.
    2) [yellow]API[/yellow]: a FastAPI project with Logfire.
    3) [yellow]AGENTS[/yellow]: an AI Agent project with PydanticAI and Logfire.
    4) [yellow]DL[/yellow]: a Deep Learning project with PyTorch.
    5) [yellow]API-AGENTS[/yellow]: a FastAPI and PydanticAI project (API and AGENTS).
    6) [yellow]API-DL[/yellow]: a Deep Learning API project (API and DL).
    7) [yellow]ALL[/yellow]: a Deep Learning, API, AI Agent project (DL and API-AGENTS).
    """
    try:
        path = Path(Path.cwd(), project_name)
        if path.exists():
            raise typer.Exit(code=CommonErrorCodes.PROJECT_EXISTS)

        method = CreateCommand(
            project_name,
            project_type,
            path,
            ci_deps,
        )
        method.build()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.callback()
def callback():
    """
    Welcome to [yellow]forgepy[/yellow]! Create a new project with the [green]forgepy create[/green] command.
    """


if __name__ == "__main__":
    app()
