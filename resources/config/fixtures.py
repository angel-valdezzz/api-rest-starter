"""pytest composition: settings, real application lifecycle, HTTP sessions and test data."""

from contextlib import nullcontext

import pytest
from requests import Session

from resources.config.application import local_application
from resources.config.settings import ApiSettings
from resources.config.test_data import default_user
from resources.services.users import UsersService


def pytest_addoption(parser):
    parser.addoption("--local-api", action="store_true", help="Start installed Demo Users API")


@pytest.fixture(scope="session")
def api_settings(pytestconfig):
    try:
        manager = (
            local_application() if pytestconfig.getoption("--local-api")
            else nullcontext(ApiSettings.from_environment())
        )
        with manager as settings:
            yield settings
    except ValueError as error:
        raise pytest.UsageError(
            "Use --local-api or configure DEMO_BASE_URL and DEMO_API_KEY"
        ) from error


def service(settings: ApiSettings, key: str | None):
    session = Session()
    session.headers.update({"Accept": "application/json"})
    if key is not None:
        session.headers["X-API-Key"] = key
    return UsersService(session, settings), session


@pytest.fixture
def users(api_settings):
    client, session = service(api_settings, api_settings.api_key)
    try:
        yield client
    finally:
        try:
            client.cleanup()
        finally:
            session.close()


@pytest.fixture
def unauthenticated_users(api_settings):
    client, session = service(api_settings, None)
    try:
        yield client
    finally:
        session.close()


@pytest.fixture
def invalid_credential_users(api_settings):
    client, session = service(api_settings, "invalid")
    try:
        yield client
    finally:
        session.close()


@pytest.fixture
def user_data():
    return default_user()


@pytest.fixture
def missing_user_id():
    from uuid import uuid4

    return str(uuid4())
