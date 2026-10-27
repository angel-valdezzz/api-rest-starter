"""HTTP operations and owned-user cleanup. No business assertions or data-file access."""

import logging
from urllib.parse import quote

from requests import Response, Session

from resources.config.settings import ApiSettings

LOGGER = logging.getLogger(__name__)


class UsersService:
    def __init__(self, session: Session, settings: ApiSettings):
        self._session = session
        self._settings = settings
        self._created_ids: list[str] = []

    def _request(self, method: str, path: str, **kwargs) -> Response:
        response = self._session.request(
            method, self._settings.base_url + path, timeout=self._settings.timeout, **kwargs
        )
        LOGGER.info("%s %s -> HTTP %s", method, path, response.status_code)
        return response

    @staticmethod
    def _path(user_id: str) -> str:
        return "/users/" + quote(user_id, safe="")

    def health(self) -> Response:
        return self._request("GET", "/health")

    def create(self, payload: dict) -> Response:
        response = self._request("POST", "/users", json=payload)
        if response.status_code == 201:
            self._created_ids.append(response.json()["id"])
        return response

    def retrieve(self, user_id: str) -> Response:
        return self._request("GET", self._path(user_id))

    def search(self, **filters) -> Response:
        return self._request("GET", "/users", params=filters)

    def replace(self, user_id: str, payload: dict) -> Response:
        return self._request("PUT", self._path(user_id), json=payload)

    def patch(self, user_id: str, payload: dict) -> Response:
        return self._request("PATCH", self._path(user_id), json=payload)

    def delete(self, user_id: str) -> Response:
        return self._request("DELETE", self._path(user_id))

    def activate(self, user_id: str) -> Response:
        return self._request("POST", self._path(user_id) + "/activate")

    def deactivate(self, user_id: str) -> Response:
        return self._request("POST", self._path(user_id) + "/deactivate")

    def statistics(self) -> Response:
        return self._request("GET", "/users/statistics")

    def cleanup(self) -> None:
        failures = []
        for user_id in reversed(self._created_ids):
            try:
                response = self.delete(user_id)
                if response.status_code not in {204, 404}:
                    failures.append(f"{user_id}: HTTP {response.status_code}")
            except Exception as error:
                failures.append(f"{user_id}: {type(error).__name__}")
        self._created_ids.clear()
        if failures:
            raise RuntimeError("Cannot clean up users owned by this test: " + "; ".join(failures))
