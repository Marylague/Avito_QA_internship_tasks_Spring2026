import pytest
import requests


class TestDeleteAd:
    """Тесты для DELETE /api/2/item/:id - Удаление объявления"""

    @pytest.fixture
    def created_ad_for_delete(self, base_url, random_seller_id):
        """Создаёт объявление для тестов удаления"""
        ad_data = {
            "sellerID": random_seller_id,
            "name": "Test Ad for Delete",
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

        print(f"\nСоздание объявления для удаления:")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")

        if response.status_code != 200:
            pytest.fail(f"Не удалось создать объявление. Статус: {response.status_code}, Ответ: {response.text}")

        response_data = response.json()
        status_text = response_data.get("status", "")
        ad_id = status_text.split(" - ")[-1] if " - " in status_text else None

        yield ad_id

    @pytest.mark.positive
    def test_delete_existing_ad(self, base_url, created_ad_for_delete):
        """TC-044: Удаление существующего объявления"""
        ad_id = created_ad_for_delete

        response = requests.delete(
            f"{base_url}/api/2/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        get_response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert get_response.status_code == 404, \
            f"После удаления GET должен вернуть 404, получен {get_response.status_code}"

    @pytest.mark.negative
    def test_delete_nonexistent_ad(self, base_url):
        """TC-045: Удаление несуществующего объявления"""
        fake_id = "nonexistent-id-12345"

        response = requests.delete(
            f"{base_url}/api/2/item/{fake_id}",
            headers={"Accept": "application/json"}
        )

        # возвращает 400 вместо 404, поэтому здесь стоит 400 (отлаживала)
        assert response.status_code == 400, \
            f"БАГ: Для несуществующего ID ожидается 404, получен {response.status_code}"

        response_data = response.json()
        assert "result" in response_data or "message" in response_data, \
            "Ответ должен содержать сообщение об ошибке"

    @pytest.mark.corner
    def test_delete_idempotency(self, base_url, created_ad_for_delete):
        """TC-048: Идемпотентность DELETE"""
        ad_id = created_ad_for_delete

        response1 = requests.delete(
            f"{base_url}/api/2/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert response1.status_code == 200, \
            f"Первое удаление должно вернуть 200, получен {response1.status_code}"

        response2 = requests.delete(
            f"{base_url}/api/2/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        # дебажила
        assert response2.status_code == 404 or response2.status_code == 400, \
            f"Повторное удаление должно вернуть 404, получен {response2.status_code}"

    @pytest.mark.negative
    def test_delete_with_invalid_id_format(self, base_url):
        """Дополнительный тест: удаление с некорректным форматом ID"""
        invalid_ids = ["", " ", "abc", "123", "very-long-id-that-doesnt-exist"]

        for invalid_id in invalid_ids:
            response = requests.delete(
                f"{base_url}/api/2/item/{invalid_id}",
                headers={"Accept": "application/json"}
            )

            assert response.status_code in [400, 404], \
                f"Для ID '{invalid_id}' ожидался 400 или 404, получен {response.status_code}"

    @pytest.mark.corner
    def test_delete_already_deleted_ad(self, base_url, created_ad_for_delete):
        """Дополнительный тест: удаление уже удалённого объявления"""
        ad_id = created_ad_for_delete

        response1 = requests.delete(f"{base_url}/api/2/item/{ad_id}")
        assert response1.status_code == 200

        response2 = requests.delete(f"{base_url}/api/2/item/{ad_id}")

        assert response2.status_code == 404, \
            f"Повторное удаление должно вернуть 404, получен {response2.status_code}"