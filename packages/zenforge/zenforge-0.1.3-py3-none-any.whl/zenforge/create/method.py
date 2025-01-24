from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Optional

import shutil
import subprocess
import sys
import os

import typer

from zenforge import ProjectType, console, TEMPLATE_DIR
from zenforge.cli import (
    CommonErrorCodes,
    SetupSuccessCodes,
    create_complete_panel,
    creation_msg,
    ProgressTracker,
)
from zenforge.config import (
    DEPENDENCY_MAP,
    TEST_DEPS,
    DEV_DEPS,
    CI_DEPS,
    set_toml_settings,
)


@dataclass
class Dependencies:
    """Dependency storage."""

    core: List[str]
    test: List[str]
    dev: List[str]
    ci: Optional[List[str]] = None

    def has_dl_deps(self) -> bool:
        return True if "torch" in self.core else False


class CreateCommand:
    """
    Handles the logic for the `create` command.

    Args:
        project_name (str): the name of the project
        project_type (forgepy.ProjectType): the type of project to create
        path (pathlib.Path): the path to the project directory
        ci_deps (bool): a flag to include CI dependencies, such as `git-cliff`
    """

    def __init__(
        self,
        project_name: str,
        project_type: ProjectType,
        path: Path,
        ci_deps: bool,
    ) -> None:
        self.project_name = project_name
        self.project_type = project_type
        self.path = path
        self.ci_deps = ci_deps

        self.deps = Dependencies(
            core=DEPENDENCY_MAP[project_type],
            test=TEST_DEPS,
            dev=DEV_DEPS,
            ci=CI_DEPS if ci_deps else None,
        )

        self.tasks = CreateTasks(project_name, project_type, path, deps=self.deps)
        self.tracker = ProgressTracker(console)

    def build(self) -> None:
        """Builds the project."""
        console.print(
            creation_msg(
                self.project_name,
                self.project_type,
                self.ci_deps,
                self.deps.has_dl_deps(),
            ),
        )

        self.path.mkdir()
        os.chdir(self.path)

        tasks = self.tasks.get_tasks()
        self.tracker.execute_tasks(tasks)

        console.print(create_complete_panel(self.project_name, self.path))
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class CreateTasks:
    """Contains the tasks for the `create` command."""

    def __init__(
        self,
        project_name: str,
        project_type: str,
        path: Path,
        deps: Dependencies,
    ) -> None:
        self.project_name = project_name
        self.project_type = project_type
        self.path = path
        self.deps = deps

        self.toml_extras = set_toml_settings(
            project_name,
            ProjectType.dl_project(project_type),
        )

        self.env_name = "venv"
        self.python_path = (
            Path(f"{self.env_name}/Scripts/python.exe")
            if sys.platform == "win32"
            else Path(f"{self.env_name}/bin/python")
        )
        self.poetry_path = (
            Path(f"{self.env_name}/Scripts/poetry.exe")
            if sys.platform == "win32"
            else Path(f"{self.env_name}/bin/poetry")
        )

    def __poetry_cmd(self, cmd: list[str], *, stdout: Any = subprocess.DEVNULL) -> None:
        """A helper method to simplify running a `subprocess.check_call` with Poetry commands."""
        subprocess.check_call([str(self.poetry_path), *cmd], stdout=stdout)

    def __poetry_add_cmd(
        self,
        deps: list[str],
        *,
        group: Optional[str] = None,
        stdout: Any = subprocess.DEVNULL,
    ) -> None:
        """A helper method to simplify running a `subprocess.check_call` with `poetry add` commands."""
        args = [str(self.poetry_path), "add"]

        if group is not None:
            args.extend(["--group", group])

        args.extend(deps)
        subprocess.check_call(args, stdout=stdout)

    def __python_cmd(
        self, executable: str, *, cmd: list[str], stdout: Any = subprocess.DEVNULL
    ) -> None:
        """A helper method to simplify running a `subprocess.check_call` for Python commands."""
        subprocess.check_call([executable, "-m", *cmd], stdout=stdout)

    def _create_venv(self) -> None:
        """Creates the virtual environment."""
        try:
            self.__python_cmd(sys.executable, cmd=["venv", self.env_name])

        except subprocess.CalledProcessError as e:
            console.print(f"Error creating virtual environment: {e}")
            raise typer.Exit(code=CommonErrorCodes.UNKNOWN_ERROR)

    def _install_poetry(self) -> None:
        """Installs Poetry in the virtual environment."""
        try:
            executable = str(self.python_path)
            self.__python_cmd(executable, cmd=["pip", "install", "--upgrade", "pip"])
            self.__python_cmd(executable, cmd=["pip", "install", "poetry"])

        except subprocess.CalledProcessError as e:
            console.print(f"Error installing Poetry: {e}")
            raise typer.Exit(code=CommonErrorCodes.UNKNOWN_ERROR)

    def _create_package(self) -> None:
        """Creates a Poetry package."""
        try:
            self.__poetry_cmd(
                [
                    "init",
                    "--name",
                    self.project_name,
                    "--python",
                    ">=3.12,<4.0",
                    "--no-interaction",
                ]
            )

            shutil.copytree(
                src=TEMPLATE_DIR.joinpath("root"),
                dst=Path.cwd(),
                dirs_exist_ok=True,
            )
            os.mkdir(self.project_name)
            os.mkdir("tests")
            open(Path(Path.cwd(), self.project_name, "__init__.py"), "w").close()

        except subprocess.CalledProcessError as e:
            console.print(f"Error creating Poetry package: {e}")
            raise typer.Exit(code=CommonErrorCodes.UNKNOWN_ERROR)

    def _update_toml(self) -> None:
        """Updates the `pyproject.toml` file."""
        with open(Path(Path.cwd(), "pyproject.toml"), "a") as f:
            f.write(f"\n{self.toml_extras}")

    def _install_deps(self) -> None:
        """Installs the required dependencies into the virtual environment."""
        try:
            self.__poetry_add_cmd(self.deps.core)
            self.__poetry_add_cmd(self.deps.test, group="testing")
            self.__poetry_add_cmd(self.deps.dev, group="dev")

            if self.deps.ci is not None:
                self.__poetry_add_cmd(self.deps.ci, group="ci")

        except subprocess.CalledProcessError as e:
            console.print(f"Error installing dependencies: {e}")
            raise typer.Exit(code=CommonErrorCodes.UNKNOWN_ERROR)

    def get_tasks(self) -> list[tuple[str, Callable]]:
        """Gets the tasks to run as a list of methods."""
        return [
            ("Building [yellow]venv[/yellow]", self._create_venv),
            ("Installing [bright_blue]Poetry[/bright_blue]", self._install_poetry),
            (
                "Building [bright_blue]Poetry[/bright_blue] package",
                self._create_package,
            ),
            ("Updating [yellow]pyproject.toml[/yellow]", self._update_toml),
            ("Installing [green]dependencies[/green]", self._install_deps),
        ]
