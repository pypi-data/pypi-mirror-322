from typing import Any, Dict, Set, override

TomlSettingsType = Dict[str, Dict[str, Any]]


class TomlOptions:
    """A parent class for `pyproject.toml` settings."""

    toml_name = None

    def as_dict(self) -> TomlSettingsType:
        return {f"[{self.toml_name}]": self.__dict__}


class PoetryDependenciesExtras(TomlOptions):
    """
    Stores extra information for poetry dependencies for the `pyproject.toml` file.

    Used for installing cuda with `torch` and `torchvision`.
    """

    toml_name = "tool.poetry.dependencies"

    def __init__(self) -> None:
        self.items = {
            "torch": {"source": "pytorch"},
            "torchvision": {"source": "pytorch"},
        }

    def items_to_str_dict(self) -> Dict[str, Set[str]]:
        """Converts the values of the `self.items` dictionary into a strings."""
        str_dict = {}
        for key, d in self.items.items():
            value_str = []
            for k, v in d.items():
                value_str.append(f'{k} = "{v}"')

            str_dict[key] = {", ".join(value_str)}

        return str_dict

    @override
    def as_dict(self) -> TomlSettingsType:
        return {f"[{self.toml_name}]": self.items_to_str_dict()}


class PyTorchSource(TomlOptions):
    """
    Stores the PyTorch Poetry source details for the `pyproject.toml` file.

    These are essential for adding CUDA capabilities to `torch` and `torchvision`.
    """

    toml_name = "tool.poetry.source"

    def __init__(self) -> None:
        self.name = "pytorch"
        self.url = "https://download.pytorch.org/whl/cu121"
        self.priority = "explicit"

    @override
    def as_dict(self) -> TomlSettingsType:
        return {f"[[{self.toml_name}]]": self.__dict__}


class PytestOptions(TomlOptions):
    """
    Stores the pytest Poetry settings for the `pyproject.toml` file.

    Adds the coverage report to all basic `pytest` commands.
    """

    toml_name = "tool.pytest.ini_options"

    def __init__(self, project_name: str) -> None:
        super().__init__()

        self.addopts = f"--cov-report term-missing --cov={project_name} tests/"


class MypyOptions(TomlOptions):
    """
    Stores the MyPy Poetry settings for the `pyproject.toml` file.
    """

    toml_name = "tool.mypy"

    def __init__(self) -> None:
        super().__init__()

        self.python_version = "3.12"
        self.ignore_missing_imports = True
        self.strict = True
        self.cache_fine_grained = True
        self.plugins = ["numpy.typing.mypy_plugin", "pydantic.mypy"]


class IsortOptions(TomlOptions):
    """
    Stores the isort Poetry settings for the `pyproject.toml` file.
    """

    toml_name = "tool.isort"

    def __init__(self) -> None:
        super().__init__()

        self.profile = "black"


class BlackOptions(TomlOptions):
    """
    Stores the black Poetry settings for the `pyproject.toml` file.
    """

    toml_name = "tool.black"

    def __init__(self) -> None:
        self.line_length = 88
        self.target_version = ["py312"]

    @override
    def as_dict(self) -> TomlSettingsType:
        return {
            f"[{self.toml_name}]": {
                "line-length": self.line_length,
                "target-version": self.target_version,
            }
        }


def settings_to_toml(d: TomlSettingsType) -> str:
    """Converts a settings dict into a toml string."""
    toml_str = ""

    for header, settings in d.items():
        toml_str += f"{header}\n"

        for key, value in settings.items():
            if isinstance(value, set):
                value = str(value).replace("'", " ")
            elif isinstance(value, str):
                value = f'"{value}"'
            elif isinstance(value, bool):
                value = str(value).lower()

            toml_str += f"{key} = {value}\n"

    return toml_str


def multi_settings_to_toml(d_list: list[TomlOptions]) -> str:
    """Converts multiple TomlOptions settings into a toml string."""
    full = ""

    for item in d_list:
        full += f"{settings_to_toml(item.as_dict())}\n"

    return full


def set_toml_settings(project_name: str, dl_project: bool) -> str:
    """Sets the extra toml settings to add to the end of the `pyproject.toml` file."""
    items = [
        PytestOptions(project_name),
        MypyOptions(),
        IsortOptions(),
        BlackOptions(),
    ]

    if dl_project:
        items.insert(0, PoetryDependenciesExtras())
        items.insert(1, PyTorchSource())

    return multi_settings_to_toml(items)
