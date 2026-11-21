from app import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')

    assert response.status_code == 200
    assert b"Welcome to Flask Application" in response.data

def test_invalid_page():
    client = app.test_client()
    response = client.get('/invalid')

    assert response.status_code == 404

