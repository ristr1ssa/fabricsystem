import requests


def test_login_success():
    response = requests.post("http://127.0.0.1:8080/?")
    assert response.status_code == 200
    assert "token" in response.json()
