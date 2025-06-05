import pytest
import requests

BASE_URL = "http://0.0.0.0:8000/api"

class TestUserAPI:
    @pytest.mark.parametrize("user_id, expected_email", [
        (2, "janet.weaver@reqres.in"),
    ])
    def test_user_data(self, user_id, expected_email):
        url = f"{BASE_URL}/users/{user_id}"
        headers = {'x-api-key': 'reqres-free-v1'}

        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        body = response.json()
        assert "data" in body, "Response body does not contain 'data' key"

        data = body["data"]
        assert data["id"] == user_id, f"Expected id {user_id}, but got {data['id']}"
        assert data["email"] == expected_email, f"Expected email {expected_email}, but got {data['email']}"

    @pytest.mark.parametrize("user_id", [2])
    def test_user_data_no_api_key(self, user_id):
        url = f"{BASE_URL}/users/{user_id}"
        expected_error = "Missing API key."

        response = requests.get(url)
        body = response.json()

        assert response.status_code == 403
        assert body["error"] == expected_error

    def test_post_user(self):
        url = f"{BASE_URL}/"
        headers = {'x-api-key': 'reqres-free-v1'}
        data = {
            "name": "morpheus",
            "job": "leader"
        }

        response = requests.post(url, headers=headers, json=data)
        body = response.json()

        assert response.status_code == 201
        assert body["name"] == data["name"]
        assert body["job"] == data["job"]

    @pytest.mark.parametrize("user_id", [2, 3, 4])
    def test_delete_user(self, user_id):
        url = f"{BASE_URL}/users/{user_id}"
        headers = {'x-api-key': 'reqres-free-v1'}

        response = requests.delete(url, headers=headers)
        assert response.status_code == 204

    def test_unsuccessful_login(self):
        response = requests.post(f"{BASE_URL}/login", data={'email': 'peter@klaven'})
        assert response.status_code == 400
        assert response.json()['error'] == 'Missing password'
        assert response.headers['Content-Type'] == 'application/json; charset=utf-8'

    def test_get_user_business_logic(self):
        response = requests.get(
            url=f'{BASE_URL}/users',
            params={"page": "2"}
        )
        assert response.status_code == 200

        data = response.json()['data']
        assert data[0]['email'] == 'michael.lawson@reqres.in'
        assert data[1]['email'] == 'lindsay.ferguson@reqres.in'

    def test_get_unique_users_business_logic2(self):
        response = requests.get(
            url=f'{BASE_URL}/users',
            params={"page": "2"}
        )
        assert response.status_code == 200

        ids = [element['id'] for element in response.json()['data']]
        assert len(ids) == len(set(ids))