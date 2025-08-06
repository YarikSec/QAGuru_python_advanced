import json
from http import HTTPStatus

import pytest
import requests
from requests import Response
from my_microservice.app.models.User import User


def test_create_user(api_client, valid_user: dict):
    create_response: Response = api_client.post(f"{api_client.base_url}/users", json=valid_user)
    assert create_response.status_code == HTTPStatus.OK

    user = User.model_validate(create_response.json())
    assert user.name == valid_user["name"]
    assert user.surname == valid_user["surname"]
    assert user.birth_date == valid_user["birth_date"]

    response = api_client.get(f"{api_client.base_url}/users/{user.id}")
    assert response.status_code == HTTPStatus.OK


def test_get_all_users(api_client, create_user: User):
    response: Response = api_client.get(f"{api_client.base_url}/users")
    assert response.status_code == HTTPStatus.OK

    users: list[User] = [User.model_validate(user) for user in response.json()["items"]]
    assert len(users) > 0
    assert any(create_user.id == user.id for user in users)


def test_get_user_by_id(api_client, create_user: User):
    response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert create_user.id == user.id
    assert create_user.name == user.name


def test_update_user_by_id(api_client, create_user: User):
    get_response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert get_response.status_code == HTTPStatus.OK
    update_user = {
        "name": "Yarik",
        "surname": "Slip",
        "birth_date": "05.10.1993",
        "products": []
    }

    update_response: Response = api_client.patch(f"{api_client.base_url}/users/{create_user.id}", json=update_user)
    assert get_response.status_code == HTTPStatus.OK

    up_user: User = User.model_validate(update_response.json())
    assert create_user.id == up_user.id
    assert update_user.get("name") == up_user.name
    assert update_user.get("surname") == up_user.surname

    response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert get_response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert update_user.get("name") == user.name
    assert update_user.get("surname") == user.surname


@pytest.mark.skip(reason="Рабочий тест, но на доработке")
@pytest.mark.parametrize("user_id", [99999])
def test_get_nonexistent_user(api_client, user_id):
    response: Response = api_client.get(f"{api_client.base_url}/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip(reason="Рабочий тест, но на доработке")
@pytest.mark.parametrize("user_id", [99999])
def test_delete_nonexistent_user(api_client, user_id):
    response: Response = api_client.delete(f"{api_client.base_url}/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_nonexistent_user(api_client, valid_user):
    response: Response = api_client.patch(f"{api_client.base_url}/users/99999", json=valid_user)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(api_client, create_user: User):
    response: Response = api_client.delete(f"{api_client.base_url}/users/{create_user.id}")
    assert response.status_code == HTTPStatus.OK

    user = User.model_validate(response.json())
    assert create_user.id == user.id

    get_response = api_client.get(f"{api_client.base_url}/users/{user.id}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_create_user_invalid_data(api_client, invalid_user: dict):
    response: Response = api_client.post(f"{api_client.base_url}/users", json=invalid_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
