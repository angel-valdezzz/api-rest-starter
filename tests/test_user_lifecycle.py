import pytest

from resources.assertions import users as check
from resources.config.test_data import user_scenarios

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("user_data", user_scenarios(), ids=lambda row: row.name)
def test_user_can_be_created_consulted_replaced_and_removed(users, user_data):
    user_id = check.user_created(users.create(user_data.create), user_data.create)

    check.user_matches(users.retrieve(user_id), user_data.create, user_id)
    check.user_inactive(users.patch(user_id, user_data.deactivation), user_id)
    check.user_replaced(
        users.replace(user_id, user_data.replacement), user_data.replacement, user_id
    )
    check.user_deleted(users.delete(user_id))
    check.user_missing(users.retrieve(user_id))


def test_duplicate_email_is_rejected(users, user_data):
    check.user_created(users.create(user_data.create), user_data.create)

    check.conflict(users.create(user_data.create))


def test_activation_conflicts_and_inactive_filters(users, user_data):
    user_id = check.user_created(users.create(user_data.create), user_data.create)

    check.conflict(users.activate(user_id))
    check.user_inactive(users.deactivate(user_id), user_id)
    check.conflict(users.deactivate(user_id))
    check.search_contains(
        users.search(role=user_data.create["role"], active=False),
        user_id,
        {"role": user_data.create["role"], "active": False},
    )
    check.user_active(users.activate(user_id), user_id)


def test_user_statistics_reflect_created_users(users, user_data):
    before = users.statistics()
    check.user_created(users.create(user_data.create), user_data.create)

    check.statistics_increased(before, users.statistics(), created=1)


def test_combined_filters_and_pagination(users, user_data):
    user_id = check.user_created(users.create(user_data.create), user_data.create)

    check.search_contains(
        users.search(role=user_data.create["role"], active=True),
        user_id,
        {"role": user_data.create["role"], "active": True},
    )
    check.pagination_matches(users.search(limit=1, offset=1), limit=1, offset=1)
