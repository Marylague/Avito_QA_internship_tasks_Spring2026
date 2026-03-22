import pytest
import requests


class TestGetSellerAds:
    """Тесты для GET /api/1/:sellerID/item - Получение объявлений продавца"""

    @pytest.mark.positive
    def test_get_existing_seller_ads(self, base_url, random_seller_id):
        """TC-030: Получение объявлений существующего продавца"""
        seller_id = random_seller_id

        ad_ids = []
        for i in range(3):
            ad_data = {
                "sellerId": seller_id,
                "name": f"Seller Ad {i}",
                "price": 100 * (i + 1)
            }
            response = requests.post(
                f"{base_url}/api/1/item",
                json=ad_data,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            ad_ids.append(response.json()["id"])

        get_response = requests.get(
            f"{base_url}/api/1/{seller_id}/item",
            headers={"Accept": "application/json"}
        )

        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data) == 3

        for ad in data:
            assert ad["sellerId"] == seller_id

    @pytest.mark.positive
    def test_get_seller_no_ads(self, base_url, random_seller_id):
        """TC-031: Получение объявлений продавца без объявлений"""
        response = requests.get(
            f"{base_url}/api/1/{random_seller_id}/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.negative
    def test_get_seller_invalid_id(self, base_url):
        """TC-036: Получение с текстовым sellerId"""
        response = requests.get(
            f"{base_url}/api/1/abc/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 400

    @pytest.mark.negative
    def test_get_seller_zero_id(self, base_url):
        """TC-034: Получение с sellerId=0"""
        response = requests.get(
            f"{base_url}/api/1/0/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 400