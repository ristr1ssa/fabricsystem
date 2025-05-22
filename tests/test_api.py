import requests


def test_login_success():
    response = requests.get("https://clck.ru/3MD2N3")
    assert response.status_code == 200
