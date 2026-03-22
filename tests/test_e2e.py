import pytest
import requests


class TestE2E:
    """E2E тесты для полного жизненного цикла объявлений"""

    @pytest.mark.e2e
    def test_full_ad_lifecycle(self, base_url, random_seller_id):
        """TC-E2E-001: Полный жизненный цикл объявления"""
        seller_id = random_seller_id

        ad_data = {
            "sellerId": seller_id,
            "name": f"E2E Test Ad",
            "price": 5000
        }
        create_response = requests.post(
            f"{base_url}/api/1/item",
            json=ad_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 200
        created_ad = create_response.json()
        ad_id = created_ad["id"]

        get_response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert get_response.status_code == 200
        retrieved_ad = get_response.json()[0] if isinstance(get_response.json(), list) else get_response.json()
        assert retrieved_ad["id"] == ad_id
        assert retrieved_ad["name"] == ad_data["name"]
        assert retrieved_ad["price"] == ad_data["price"]
        assert retrieved_ad["sellerId"] == seller_id

        stats_response = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert stats_response.status_code == 200
        stats = stats_response.json()[0]
        assert "viewCount" in stats
        assert "likes" in stats
        assert "contacts" in stats

        seller_ads_response = requests.get(
            f"{base_url}/api/1/{seller_id}/item",
            headers={"Accept": "application/json"}
        )
        assert seller_ads_response.status_code == 200
        seller_ads = seller_ads_response.json()
        assert len(seller_ads) >= 1
        found = any(ad["id"] == ad_id for ad in seller_ads)
        assert found, "Created ad not found in seller's ads"

        delete_response = requests.delete(
            f"{base_url}/api/2/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert delete_response.status_code == 200

        get_deleted_response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert get_deleted_response.status_code == 404

    @pytest.mark.e2e
    def test_multiple_ads_same_seller(self, base_url, random_seller_id):
        """TC-E2E-002: Создание нескольких объявлений и проверка продавца"""
        seller_id = random_seller_id
        created_ids = []
        ad_names = []

        for i in range(3):
            ad_data = {
                "sellerId": seller_id,
                "name": f"Multiple Ad {i}",
                "price": 1000 * (i + 1)
            }
            response = requests.post(
                f"{base_url}/api/1/item",
                json=ad_data,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            created_ad = response.json()
            created_ids.append(created_ad["id"])
            ad_names.append(created_ad["name"])

        response = requests.get(
            f"{base_url}/api/1/{seller_id}/item",
            headers={"Accept": "application/json"}
        )
        assert response.status_code == 200
        seller_ads = response.json()

        assert len(seller_ads) == 3

        seller_ad_ids = [ad["id"] for ad in seller_ads]
        for ad_id in created_ids:
            assert ad_id in seller_ad_ids

    @pytest.mark.e2e
    def test_view_count_increments(self, base_url, created_ad):
        """TC-E2E-003: Влияние просмотра на статистику"""
        ad_id = created_ad["id"]

        initial_stats = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert initial_stats.status_code == 200
        initial_views = initial_stats.json()[0]["viewCount"]

        for _ in range(3):
            requests.get(
                f"{base_url}/api/1/item/{ad_id}",
                headers={"Accept": "application/json"}
            )

        updated_stats = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert updated_stats.status_code == 200
        updated_views = updated_stats.json()[0]["viewCount"]

        assert updated_views == initial_views + 3