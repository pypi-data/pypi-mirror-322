import importlib.resources as pkg_resources
from enum import StrEnum

from rich.console import Console

console = Console()

PKG_DIR = pkg_resources.files(__package__)
TEMPLATE_DIR = PKG_DIR.joinpath("template")


class ProjectType(StrEnum):
    """Different types of projects."""

    BASIC = "basic"
    API = "api"
    API_AGENTS = "api-agents"
    AGENTS = "agents"
    DEEP_LEARNING = "dl"
    API_DEEP_LEARNING = "api-dl"
    ALL = "all"

    @staticmethod
    def dl_project(value: str) -> bool:
        """Checks if the value is a Deep Learning project."""
        if "dl" in value or value == "all":
            return True

        return False


__all__ = [
    "ProjectType",
    "console",
    "PKG_DIR",
    "TEMPLATE_DIR",
]
