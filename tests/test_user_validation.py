import pytest

from resources.assertions import users as check
from resources.config.test_data import invalid_users, pagination_cases

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("scenario", invalid_users(), ids=lambda row: row.name)
def test_invalid_user_data_is_rejected(users, scenario):
    check.invalid_input(users.create(scenario.payload), scenario.expected_status)


@pytest.mark.parametrize("filters", pagination_cases())
def test_invalid_pagination_is_rejected(users, filters):
    check.invalid_input(users.search(**filters))


def test_null_patch_does_not_modify_the_user(users, user_data):
    user_id = check.user_created(users.create(user_data.create), user_data.create)

    check.invalid_input(users.patch(user_id, user_data.null_patch))
    check.user_matches(users.retrieve(user_id), user_data.create, user_id)


def test_public_health_and_missing_credentials(unauthenticated_users):
    check.healthy(unauthenticated_users.health())
    check.unauthorized(unauthenticated_users.search())


def test_invalid_credentials_are_rejected(invalid_credential_users):
    check.unauthorized(invalid_credential_users.search())


def test_missing_user_is_reported(users, missing_user_id):
    check.user_missing(users.retrieve(missing_user_id))
