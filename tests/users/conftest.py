import os
from uuid import uuid4
import pytest
import requests

@pytest.fixture
def api():
    base = os.environ['DEMO_BASE_URL'].rstrip('/')
    session = requests.Session()
    session.headers['X-API-Key'] = os.environ['DEMO_API_KEY']
    created = []
    def request(method, path, **kwargs):
        return session.request(method, base + path, timeout=15, **kwargs)
    def create(**extra):
        payload = dict(name='Automation', email=uuid4().hex+'@example.com', role='sales', active=True)
        payload.update(extra)
        response = request('POST', '/users', json=payload)
        assert response.status_code == 201
        user = response.json()
        created.append(user['id'])
        assert response.headers['Location'] == '/users/' + user['id']
        assert all(user[k] == v for k,v in payload.items())
        return user
    yield request, create
    try:
        for user_id in created:
            assert request('DELETE', '/users/'+user_id).status_code in (204,404)
    finally:
        session.close()
