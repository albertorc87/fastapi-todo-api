from fastapi.testclient import TestClient
from main import app

def test_create_user_ok():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_ok@cosasdedevs.com',
        'username': 'test_create_user_ok',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['email'] == user['email']
    assert data['username'] == user['username']

def test_create_user_duplicate_email():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_duplicate_email@cosasdedevs.com',
        'username': 'test_create_user_duplicate_email',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text

    user['username'] = 'test_create_user_duplicate_email2'

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Email already registered'


def test_create_user_duplicate_username():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_duplicate_username@cosasdedevs.com',
        'username': 'test_create_user_duplicate_username',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Username already registered'