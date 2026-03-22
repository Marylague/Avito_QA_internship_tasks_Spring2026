import pytest
import requests


class TestGetAd:
    """Тесты для GET /api/1/item/:id - Получение объявления по ID"""

    @pytest.mark.positive
    def test_get_existing_ad(self, base_url, created_ad):
        """TC-022: Получение существующего объявления"""
        ad_id = created_ad["id"]
        response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        ad = data[0] if isinstance(data, list) else data
        assert ad["id"] == ad_id
        assert ad["sellerId"] == created_ad["data"]["sellerId"]
        assert ad["name"] == created_ad["data"]["name"]
        assert ad["price"] == created_ad["data"]["price"]

    @pytest.mark.negative
    def test_get_nonexistent_ad(self, base_url):
        """TC-025: Получение по несуществующему ID"""
        fake_id = "nonexistent-id-12345"
        response = requests.get(
            f"{base_url}/api/1/item/{fake_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 404

    @pytest.mark.negative
    def test_get_ad_invalid_id_format(self, base_url):
        """TC-027: Получение по некорректному формату ID"""
        response = requests.get(
            f"{base_url}/api/1/item/abc",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 400 or response.status_code == 404

    @pytest.mark.corner
    def test_get_deleted_ad(self, base_url, created_ad):
        """TC-029: Получение удалённого объявления"""
        ad_id = created_ad["id"]
        delete_response = requests.delete(f"{base_url}/api/2/item/{ad_id}")
        assert delete_response.status_code == 200

        get_response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert get_response.status_code == 404