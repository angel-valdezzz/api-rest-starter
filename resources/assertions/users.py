"""Business checks over the real response. Each check executes once and retains failure context."""

from uuid import UUID

from requests import Response


def status_is(response: Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"{response.request.method} {response.request.path_url}: "
        f"expected HTTP {expected}, got {response.status_code}; {response.text[:500]}"
    )


def user_matches(response: Response, expected: dict, user_id: str | None = None) -> dict:
    status_is(response, 200)
    actual = response.json()
    for field, value in expected.items():
        assert actual[field] == value, f"Unexpected user field {field}"
    UUID(actual["id"])
    if user_id is not None:
        assert actual["id"] == user_id
    return actual


def user_created(response: Response, expected: dict) -> str:
    status_is(response, 201)
    actual = response.json()
    UUID(actual["id"])
    for field, value in expected.items():
        assert actual[field] == value, f"Created user has unexpected {field}"
    assert response.headers["Location"] == "/users/" + actual["id"]
    return actual["id"]


def user_replaced(response: Response, expected: dict, user_id: str) -> None:
    actual = user_matches(response, expected, user_id)
    assert actual["role"] == "support"
    assert actual["active"] is True


def user_inactive(response: Response, user_id: str) -> None:
    actual = user_matches(response, {"active": False}, user_id)
    assert actual["active"] is False


def user_active(response: Response, user_id: str) -> None:
    user_matches(response, {"active": True}, user_id)


def user_deleted(response: Response) -> None:
    status_is(response, 204)
    assert response.content == b""


def user_missing(response: Response) -> None:
    status_is(response, 404)


def conflict(response: Response) -> None:
    status_is(response, 409)
    assert response.json()["detail"]


def invalid_input(response: Response, expected: int = 422) -> None:
    status_is(response, expected)
    assert isinstance(response.json()["detail"], list)


def unauthorized(response: Response) -> None:
    status_is(response, 401)
    assert response.json()["detail"] == "Invalid or missing API key"


def healthy(response: Response) -> None:
    status_is(response, 200)
    assert response.json() == {"status": "ok", "storage": "temporary"}


def search_contains(response: Response, user_id: str, expected: dict) -> None:
    status_is(response, 200)
    items = response.json()["items"]
    assert user_id in {item["id"] for item in items}
    assert all(all(item[key] == value for key, value in expected.items()) for item in items)


def pagination_matches(response: Response, limit: int, offset: int) -> None:
    status_is(response, 200)
    page = response.json()
    assert page["limit"] == limit
    assert page["offset"] == offset
    assert len(page["items"]) <= limit


def statistics_increased(before: Response, after: Response, created: int) -> None:
    status_is(before, 200)
    status_is(after, 200)
    assert after.json()["total"] == before.json()["total"] + created
