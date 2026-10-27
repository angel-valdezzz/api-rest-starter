from resources.config.settings import ApiSettings
from resources.config.test_data import default_user, template, user_scenarios


def test_rows_prepare_unique_users_without_changing_template():
    original = template("create-user.json")
    first = user_scenarios()
    second = user_scenarios()

    assert [row.create["role"] for row in first] == ["support", "sales"]
    assert first[0].create["email"] != second[0].create["email"]
    assert template("create-user.json") == original
    assert original["email"] == ""


def test_boolean_and_null_payloads_preserve_json_types():
    scenario = default_user()
    assert scenario.deactivation["active"] is False
    assert scenario.null_patch["name"] is None


def test_credentials_are_not_in_settings_representation():
    secret = "only-for-this-unit-check"
    assert secret not in repr(ApiSettings("http://127.0.0.1:8000", secret))
