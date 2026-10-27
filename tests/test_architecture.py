"""Executable dependency rules for the accepted Robot API architecture."""

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def imported_modules(source: str) -> set[str]:
    result = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


def violations(source: str, forbidden: tuple[str, ...]) -> set[str]:
    return {
        name for name in imported_modules(source)
        if any(name == prefix or name.startswith(prefix + ".") for prefix in forbidden)
    }


@pytest.mark.parametrize("path", sorted((ROOT / "tests").glob("test_user_*.py")), ids=lambda p: p.name)
def test_scenarios_do_not_access_http_or_infrastructure(path):
    source = path.read_text(encoding="utf-8")
    assert not violations(source, (
        "requests", "httpx", "urllib", "demo_api", "resources.services",
        "resources.config.application", "resources.config.fixtures", "pathlib", "json", "csv",
    )), path
    assert not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))), (
        "Business assertions belong in resources/assertions", path
    )


def test_services_do_not_load_data_or_assert_business_results():
    for path in (ROOT / "resources" / "services").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert not violations(source, (
            "pathlib", "csv", "json", "pytest", "resources.assertions",
            "resources.config.application", "resources.config.test_data",
        )), path
        assert not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))), path


def test_assertions_do_not_execute_requests_or_load_fixtures():
    for path in (ROOT / "resources" / "assertions").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert not violations(source, ("resources.services", "resources.config", "demo_api")), path
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "requests":
                assert {alias.name for alias in node.names} <= {"Response"}, path
            if isinstance(node, ast.Import):
                assert not any(alias.name == "requests" for alias in node.names), path


@pytest.mark.parametrize("source", [
    "import requests as client",
    "from requests import Session",
    "import resources.services.users",
    "from resources.config.application import local_application",
])
def test_layer_guard_detects_forbidden_imports_even_with_aliases(source):
    assert violations(source, ("requests", "resources.services", "resources.config.application"))
