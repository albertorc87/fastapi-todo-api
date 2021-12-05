from fastapi.testclient import TestClient
from main import app


def create_user_and_make_login(username: str):
    client = TestClient(app)

    user = {
        'email': f'{username}@cosasdedevs.com',
        'username': username,
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )

    login = {
        'username': username,
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/login/',
        data=login,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )

    data = response.json()
    return data['access_token']


def test_create_todo_ok():
    token = create_user_and_make_login('test_create_todo_ok')

    client = TestClient(app)

    todo = {
        'title': 'My first task'
    }

    response = client.post(
        '/api/v1/to-do/',
        json=todo,
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data['title'] == todo['title']
    assert data['is_done'] == False