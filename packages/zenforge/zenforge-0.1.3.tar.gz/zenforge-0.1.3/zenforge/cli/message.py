from typing import Dict
from enum import Enum
import textwrap

import typer

from rich.console import Console
from rich.panel import Panel

from zenforge.cli.codes import SetupSuccessCodes, CommonErrorCodes


# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
MAGIC = ":sparkles:"

# Core URLs
GITHUB_ROOT = "https://github.com/Achronus/forgepy"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"


# Messages
MORE_HELP_INFO = f"""
[red]Really stuck?[/red] 
  Report the issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

UNKNOWN_ERROR = f"""
{FAIL} 🥴 Well this is awkward... We didn't account for this! 🥴 {FAIL}

You've encountered something unexpected 🤯. Please report this issue on [bright_blue][link={GITHUB_ISSUES_URL}]GitHub[/link][/bright_blue].
"""


def creation_msg(
    project_name: str,
    project_type: str,
    ci_deps: bool,
    dl_deps: bool,
) -> str:
    extra = ""

    if dl_deps:
        extra = "\n❗ Warning: PyTorch added to dependencies with CUDA. May take extra time to create.\n"

    return f"\n{MAGIC} Creating new [magenta]{project_type}[/magenta] project called [green]{project_name}[/green] with [yellow]ci_deps={ci_deps}[/yellow] {MAGIC}\n{extra}"


def error_msg_with_checks(title: str, desc: str) -> str:
    """Formats error messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{FAIL} [bright_red]{title}[/bright_red] {FAIL}\n") + desc


def success_msg_with_checks(title: str, desc: str, icon: str = MAGIC) -> str:
    """Formats success messages that have a title and a list of checks."""
    return (
        textwrap.dedent(f"\n{icon} [bright_green]{title}[/bright_green] {icon}\n")
        + desc
    )


# Message mappings
SUCCESS_MSG_MAP = {
    SetupSuccessCodes.TEST_SUCCESS: success_msg_with_checks("Test", desc=""),
    SetupSuccessCodes.COMPLETE: "",
    SetupSuccessCodes.ALREADY_CONFIGURED: "",
}


COMMON_ERROR_MAP = {
    CommonErrorCodes.TEST_ERROR: error_msg_with_checks("Test", desc=""),
    CommonErrorCodes.PROJECT_EXISTS: error_msg_with_checks(
        "Project already exists!",
        desc="\nPlease choose another name or move the existing project.\n",
    ),
}


MSG_MAPPER = {
    **SUCCESS_MSG_MAP,
    **COMMON_ERROR_MAP,
}


class MessageHandler:
    """Handles all the error and success messages for the CLI."""

    def __init__(self, console: Console, msg_mapper: Dict[Enum, str]) -> None:
        self.console = console
        self.msg_mapper = msg_mapper

    @staticmethod
    def __error_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles error messages and returns a panel with their information."""
        err_str = "[cyan]Error code[/cyan]"
        error_code = f"\n{err_str}: {e.exit_code.value}\n"

        return Panel(
            msg + MORE_HELP_INFO + error_code,
            expand=False,
            border_style="bright_red",
        )

    @staticmethod
    def __success_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles success messages and returns a panel with their information."""
        return Panel(msg, expand=False, border_style="bright_green")

    def msg(self, e: typer.Exit) -> None:
        """Assigns a success or error message depending on the code received."""
        try:
            if e.exit_code not in self.msg_mapper.keys():
                e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

            msg = textwrap.dedent(self.msg_mapper.get(e.exit_code, UNKNOWN_ERROR))

        except AttributeError:
            e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

        msg_type = e.exit_code.__class__.__name__

        if msg != "":
            panel = (
                self.__error_msg(msg, e)
                if "Error" in msg_type
                else self.__success_msg(msg, e)
            )
            self.console.print(panel)
