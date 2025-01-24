import textwrap
import time
from typing import Callable, List, Tuple

from zenforge.cli.message import MAGIC, PASS

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


def create_panel(
    text: str,
    colour: str = "bright_green",
    padding: tuple[int, int] = (0, 4),
) -> Panel:
    """A utility function for building panels."""
    return Panel.fit(
        textwrap.dedent(text),
        border_style=colour,
        padding=padding,
    )


def success_panel(title: str, desc: str = "") -> Panel:
    return create_panel(f"""
    {MAGIC} [bright_green]{title}[/bright_green] {MAGIC}
    {desc}""")


def create_complete_panel(project_name: str, path: str) -> Panel:
    """Creates a printable panel after successfully completing the `create` command."""
    return success_panel(
        f"Project [magenta][link={path}]{project_name}[/link][/magenta] created successfully!"
    )


class ProgressTracker:
    """A custom progress tracker for task completion."""

    def __init__(self, console: Console) -> None:
        self.console = console

        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
            console=console,
        )
        self._current_task_id = None

    def execute_tasks(self, tasks: List[Tuple[str, Callable]]) -> None:
        """Executes a list of tasks."""
        try:
            with self.progress:
                for desc, task_func in tasks:
                    self._current_task_id = self.progress.add_task(
                        description=desc,
                        total=1,
                    )

                    task_func()

                    self.progress.update(
                        self._current_task_id,
                        description=f"{PASS} {desc}",
                        completed=True,
                    )
                    time.sleep(1)
        finally:
            self._current_task_id = None
