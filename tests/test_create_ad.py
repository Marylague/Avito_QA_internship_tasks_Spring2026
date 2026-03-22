import pytest
import requests


class TestCreateAd:
    """Тесты для POST /api/1/item - Создание объявления"""

    @pytest.mark.positive
    def test_create_ad_minimal_valid_data(self, base_url, random_seller_id):
        """TC-001: Создание объявления с минимальными валидными данными"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Test Ad",
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }

        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nОтвет сервера: {response.text}")

        assert response.status_code == 200

        response_data = response.json()
        assert "status" in response_data
        assert "Сохранили объявление" in response_data["status"]

        ad_id = response_data["status"].split(" - ")[-1]
        assert ad_id, "ID не найден в ответе"

    @pytest.mark.positive
    def test_create_ad_with_statistics(self, base_url, random_seller_id):
        """TC-002: Создание объявления со статистикой"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Ad With Stats",
            "price": 1000,
            "likes": 10,
            "viewCount": 100,
            "contacts": 5
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data
        assert "Сохранили объявление" in response_data["status"]

    @pytest.mark.positive
    def test_create_ad_price_zero(self, base_url, random_seller_id):
        """TC-003: Создание объявления с price = 0"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Free Ad",
            "price": 0,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data

    @pytest.mark.positive
    def test_create_ad_price_max(self, base_url, random_seller_id):
        """TC-004: Создание объявления с максимальной ценой"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Expensive Ad",
            "price": 999999999,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data

    @pytest.mark.positive
    def test_create_ad_name_one_char(self, base_url, random_seller_id):
        """TC-005: Создание объявления с name из 1 символа"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "A",
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data

    @pytest.mark.positive
    def test_create_ad_name_long(self, base_url, random_seller_id):
        """TC-006: Создание объявления с длинным name (100 символов)"""
        long_name = "A" * 100
        ad_data = {
            "sellerID": random_seller_id,
            "name": long_name,
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data

    @pytest.mark.negative
    def test_create_ad_missing_seller_id(self, base_url):
        """TC-007: Создание без поля sellerID"""
        ad_data = {
            "name": "No Seller",
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_missing_name(self, base_url, random_seller_id):
        """TC-008: Создание без поля name"""
        ad_data = {
            "sellerID": random_seller_id,
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_missing_price(self, base_url, random_seller_id):
        """TC-009: Создание без поля price"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "No Price",
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_missing_likes(self, base_url, random_seller_id):
        """TC-XXX: Создание без обязательного поля likes"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Missing Likes",
            "price": 100,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400
        response_data = response.json()
        assert "likes обязательно" in response_data.get("result", {}).get("message", "")

    @pytest.mark.negative
    def test_create_ad_empty_body(self, base_url):
        """TC-010: Создание с пустым телом запроса"""
        response = requests.post(
            f"{base_url}/api/1/item",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_negative_price(self, base_url, random_seller_id):
        """TC-013: Создание с отрицательной ценой"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Negative Price",
            "price": -100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_price_string(self, base_url, random_seller_id):
        """TC-014: Создание с price не числом"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "String Price",
            "price": "not a number",
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_create_ad_empty_name(self, base_url, random_seller_id):
        """TC-015: Создание с пустым name"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "",
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.corner
    def test_create_ad_idempotency(self, base_url, random_seller_id):
        """TC-018: Идемпотентность - два одинаковых запроса создают разные объявления"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Idempotent Test",
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }

        response1 = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )
        response2 = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        id1 = response1.json()["status"].split(" - ")[-1]
        id2 = response2.json()["status"].split(" - ")[-1]

        assert id1 != id2

    @pytest.mark.corner
    def test_create_ad_special_characters(self, base_url, random_seller_id):
        """TC-021: Создание со спецсимволами в name"""
        special_name = "!@#$%^&*()_+{}|:<>?~`"
        ad_data = {
            "sellerID": random_seller_id,
            "name": special_name,
            "price": 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
        response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data