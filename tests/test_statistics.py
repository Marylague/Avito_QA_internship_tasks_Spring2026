import pytest
import requests


class TestStatistics:
    """Тесты для статистики (GET /api/1/statistic/:id и /api/2/statistic/:id)"""

    @pytest.mark.positive
    def test_get_statistics_v1(self, base_url, created_ad):
        """TC-038: Получение статистики существующего объявления v1"""
        ad_id = created_ad["id"]
        response = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "likes" in data[0]
        assert "viewCount" in data[0]
        assert "contacts" in data[0]

    @pytest.mark.positive
    def test_get_statistics_v2(self, base_url, created_ad):
        """TC-039: Получение статистики существующего объявления v2"""
        ad_id = created_ad["id"]
        response = requests.get(
            f"{base_url}/api/2/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data is not None

    @pytest.mark.positive
    def test_view_count_increments(self, base_url, created_ad):
        """TC-040: Проверка увеличения просмотров"""
        ad_id = created_ad["id"]

        stats_response = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert stats_response.status_code == 200
        initial_view_count = stats_response.json()[0]["viewCount"]

        for _ in range(3):
            requests.get(
                f"{base_url}/api/1/item/{ad_id}",
                headers={"Accept": "application/json"}
            )

        updated_stats_response = requests.get(
            f"{base_url}/api/1/statistic/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert updated_stats_response.status_code == 200
        updated_view_count = updated_stats_response.json()[0]["viewCount"]

        assert updated_view_count == initial_view_count + 3

    @pytest.mark.negative
    def test_get_statistics_nonexistent(self, base_url):
        """TC-041: Получение статистики по несуществующему ID"""
        fake_id = "nonexistent-id-12345"
        response = requests.get(
            f"{base_url}/api/1/statistic/{fake_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 404