import pytest
import requests
import concurrent.futures
import time


class TestPerformance:
    """Производительностные тесты"""

    @pytest.mark.performance
    def test_concurrent_creates(self, base_url, random_seller_id):
        """Проверка параллельного создания объявлений"""
        seller_id = random_seller_id

        def create_ad(i):
            ad_data = {
                "sellerId": seller_id,
                "name": f"Concurrent Ad {i}",
                "price": 100
            }
            return requests.post(
                f"{base_url}/api/1/item",
                json=ad_data,
                headers={"Content-Type": "application/json"}
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_ad, i) for i in range(10)]
            results = [f.result() for f in futures]

        successful = sum(1 for r in results if r.status_code == 200)
        assert successful == 10, f"Only {successful}/10 ads created successfully"