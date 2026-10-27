"""Load the scenario matrices and prepare a fresh execution copy of valid JSON templates."""

import csv
import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


@dataclass(frozen=True)
class UserScenario:
    name: str
    create: dict
    replacement: dict
    deactivation: dict
    null_patch: dict

    def with_email(self, email: str) -> dict:
        payload = deepcopy(self.create)
        payload["email"] = email
        return payload


@dataclass(frozen=True)
class InvalidUserScenario:
    name: str
    payload: dict
    expected_status: int


def template(name: str) -> dict:
    return json.loads((DATA / "payloads" / name).read_text(encoding="utf-8"))


def user_scenarios() -> list[UserScenario]:
    with (DATA / "tables" / "users.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    result = []
    for row in rows:
        payload = template("create-user.json")
        payload.update(name=row["name"], role=row["role"], email=f"qa-{uuid4().hex}@example.com")
        replacement = template("replace-user.json")
        replacement["email"] = f"qa-{uuid4().hex}@example.com"
        result.append(
            UserScenario(
                row["scenario"],
                payload,
                replacement,
                template("deactivate-user.json"),
                template("null-patch.json"),
            )
        )
    return result


def default_user() -> UserScenario:
    return user_scenarios()[0]


def invalid_users() -> list[InvalidUserScenario]:
    cases = json.loads((DATA / "test" / "invalid_users.json").read_text(encoding="utf-8"))
    return [
        InvalidUserScenario(row["name"], row["payload"], row["expected_status"]) for row in cases
    ]


def pagination_cases() -> list[dict]:
    return json.loads((DATA / "test" / "invalid_pagination.json").read_text(encoding="utf-8"))
