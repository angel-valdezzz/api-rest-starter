# API automation architecture

Follow robotframework-api-testing: scenarios, services, assertions, configuration and input/payload data.
tests/test_user_*.py compose business calls and semantic assertions, without requests or raw assertions.
resources/services owns endpoints and HTTP, never fixture/file loading or business assertions.
resources/assertions inspects responses, never executes requests.
resources/config owns settings, composition, lifecycle, fixtures and data preparation.
Poetry and poetry.lock are authoritative. Execute the real demo-users-api, never a substitute server.
Old synthetic starter content belongs under legacy/http-starter, outside default collection.
Run architectural/unit checks, Ruff and real integration before recording validation.
