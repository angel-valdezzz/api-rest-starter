# Python · pytest · Requests — Demo Users API

[Español](README.es.md)

Independent API automation following the established
[Robot API architecture](https://github.com/angel-valdezzz/robotframework-api-testing/blob/main/docs/architecture.md).
Scenarios, HTTP services, business assertions, configuration and input/payload data have separate responsibilities.

## Install and run

Python 3.12–3.14 and Poetry 2.5.1. Run from the repository root:

```powershell
poetry sync
poetry run pytest --local-api --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

`--local-api` starts the actual separate FastAPI project installed from the commit in pyproject.toml/poetry.lock.
No HTTP endpoints or fake application are implemented inside this example.
For an existing deployment, set DEMO_BASE_URL and DEMO_API_KEY in your shell and omit --local-api.
Use a dedicated testing credential and fictional data.

```powershell
$env:DEMO_BASE_URL = "https://your-demo-users-api.example"
$env:DEMO_API_KEY = "<your-private-key>"
poetry run pytest -m integration
poetry run pytest -m "not integration"
poetry run ruff check resources tests
poetry run ruff format --check resources tests
```

The .env.example file is documentation; it is not loaded automatically.

## Responsibilities

| Path | Responsibility |
| --- | --- |
| tests/test_user_*.py | Business scenarios calling services and named business checks |
| resources/services/users.py | Real HTTP operations and cleanup of users created by that test |
| resources/assertions/users.py | Status, identity, state, filters, pagination and statistics checks |
| resources/config | Settings, lifecycle/composition, fixtures and data preparation |
| data/tables, data/test | Scenario matrices, validation inputs and expected outcomes |
| data/payloads | Valid JSON templates, copied for each execution |
| tests/test_architecture.py | Enforced dependency boundaries |

Services never load CSV/JSON files. Tests contain no requests, endpoint strings or raw response assertions.
API keys are excluded from settings repr and request logging; reports record method/path/status without headers.
The local API key is ephemeral. Teardown cleans only IDs created by the current case, even on failure.

[Architecture](docs/architecture.md) · [Scenario matrix](docs/scenarios.md) · [Validation](VALIDATION.md).
The previous synthetic HTTP teaching material is retained under legacy/http-starter and is not collected or started.
