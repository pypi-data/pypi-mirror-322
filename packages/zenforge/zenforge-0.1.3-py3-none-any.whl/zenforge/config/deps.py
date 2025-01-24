# project.dependencies
CORE = [
    "pydantic-settings",
]

CORE_CONDITIONAL = [
    "pydantic",
]

AGENTS = [
    "pydantic-ai-slim[logfire]",
]

API = [
    "fastapi[standard]",
    "logfire",
]

DEEP_LEARNING = [
    "torch",
    "torchvision",
    "pyyaml",
]

API_AGENTS = [
    "pydantic-ai-slim[logfire]",
    "fastapi[standard]",
]

BASIC = CORE + CORE_CONDITIONAL

DEPENDENCY_MAP = {
    "basic": BASIC,
    "agents": CORE + AGENTS,
    "api": CORE + API,
    "dl": BASIC + DEEP_LEARNING,
    "api-agents": CORE + API_AGENTS,
    "api-dl": CORE + API + DEEP_LEARNING,
    "all": CORE + API_AGENTS + DEEP_LEARNING,
}
"""Assigns dependencies based on the `ProjectType` Enum."""

# group.testing.dependencies
TEST_DEPS = [
    "pytest",
    "pytest-cov",
    "black",
    "flake8",
    "isort",
    "mypy",
    "flake8-docstrings",
    "flake8-bugbear",
]

# group.dev.dependencies
DEV_DEPS = [
    "ipykernel",
]

# group.ci.dependencies
CI_DEPS = [
    "git-cliff",
]
