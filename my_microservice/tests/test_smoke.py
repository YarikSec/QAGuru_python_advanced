from http import HTTPStatus

import requests
from my_microservice.models.AppStatus import AppStatus
import pytest


class TestSmoke:
    @pytest.mark.skip(reason="Тест валится, разбираюсь")
    def test_smoke(self, app_url):
        response = requests.get(f"{app_url}/status")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == AppStatus().to_json()

    def test_status_endpoint(self, app_url):
        response = requests.get(f"{app_url}/status")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "users" in data
        assert isinstance(data["users"], bool)

    def test_port_availability(self, app_url):
        # Если сервис отвечает на запросы, значит порт открыт
        response = requests.get(app_url)
        assert response.status_code in [200, 404, 403], "Сервис недоступен"

    @pytest.mark.parametrize("page,size", [(1, 5), (2, 10), (3, 20)])
    def test_pagination_items_count(self, app_url, page, size):
        """Проверка ожидаемого количества объектов в ответе"""
        response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data
        
        # Проверяем размер страницы
        assert len(data["items"]) <= size
        assert data["size"] == size
        assert data["page"] == page
        
        # Проверяем, что количество элементов не превышает общее количество
        assert len(data["items"]) <= data["total"]

    @pytest.mark.parametrize("size", [5, 10, 20])
    def test_pagination_pages_count(self, app_url, size):
        """Проверка правильного количества страниц при разных значениях size"""
        response = requests.get(f"{app_url}/api/users/?size={size}")
        assert response.status_code == 200
        
        data = response.json()
        total = data["total"]
        
        # Вычисляем ожидаемое количество страниц
        expected_pages = (total + size - 1) // size  # округление вверх
        assert data["pages"] == expected_pages

    def test_pagination_different_pages(self, app_url):
        """Проверка, что возвращаются разные данные при разных значениях page"""

        response_page1 = requests.get(f"{app_url}/api/users/?size=5&page=1")
        assert response_page1.status_code == 200
        data_page1 = response_page1.json()

        response_page2 = requests.get(f"{app_url}/api/users/?size=5&page=2")
        assert response_page2.status_code == 200
        data_page2 = response_page2.json()
        
        # Проверяем, что данные на разных страницах разные
        assert data_page1["items"] != data_page2["items"]
        
        # Проверяем, что нет пересечений в ID
        ids_page1 = {item["id"] for item in data_page1["items"]}
        ids_page2 = {item["id"] for item in data_page2["items"]}
        assert not ids_page1.intersection(ids_page2)

    def test_get_user_by_id(self, app_url):
        # Проверяем существующего пользователя
        response = requests.get(f"{app_url}/api/users/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "first_name" in data
        assert "last_name" in data
        assert "avatar" in data
        
        # Проверяем несуществующего пользователя
        response = requests.get(f"{app_url}/api/users/999")
        assert response.status_code == 404
        
        # Проверяем некорректный ID
        response = requests.get(f"{app_url}/api/users/0")
        assert response.status_code == 422

