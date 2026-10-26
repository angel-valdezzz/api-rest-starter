import os
from uuid import uuid4
import pytest
import requests

def test_crud(api):
    request, create = api
    user = create()
    path = '/users/'+user['id']
    assert request('GET',path).json() == user
    changed = request('PATCH',path,json={'active':False})
    assert changed.status_code == 200 and changed.json()['active'] is False
    replacement = {'name':'Replaced','email':uuid4().hex+'@example.com'}
    response = request('PUT',path,json=replacement)
    assert response.status_code == 200
    assert response.json() == dict(replacement,id=user['id'],role='support',active=True)
    assert request('DELETE',path).status_code == 204
    assert request('GET',path).status_code == 404

def test_duplicate(api):
    request, create = api
    user=create()
    assert request('POST','/users',json={'name':'Duplicate','email':user['email']}).status_code == 409

def test_lifecycle_and_filters(api):
    request, create = api
    user=create()
    path='/users/'+user['id']
    assert request('POST',path+'/activate').status_code == 409
    response=request('POST',path+'/deactivate')
    assert response.status_code == 200 and response.json()['active'] is False
    assert request('POST',path+'/deactivate').status_code == 409
    response=request('GET','/users',params={'role':'sales','active':'false','limit':100})
    assert response.status_code == 200
    assert user['id'] in [item['id'] for item in response.json()['items']]
    assert all(item['role']=='sales' and not item['active'] for item in response.json()['items'])
    assert request('POST',path+'/activate').status_code == 200

@pytest.mark.parametrize('payload',[{'name':'','email':'bad'},{'name':'A','email':'a@example.com','unknown':True},{'name':'A','email':'a@example.com','role':'owner'}])
def test_validation(api,payload):
    request,_=api
    assert request('POST','/users',json=payload).status_code == 422

def test_null_and_pagination(api):
    request,create=api
    user=create()
    assert request('PATCH','/users/'+user['id'],json={'name':None}).status_code == 422
    assert request('GET','/users?limit=0').status_code == 422

def test_auth_and_missing_user(api):
    request,_=api
    base=os.environ['DEMO_BASE_URL']
    assert requests.get(base+'/health',timeout=10).json() == {'status':'ok','storage':'temporary'}
    assert requests.get(base+'/users',timeout=10).status_code == 401
    assert request('GET','/users/'+str(uuid4())).status_code == 404
