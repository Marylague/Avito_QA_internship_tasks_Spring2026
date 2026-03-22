import pytest
import requests
import time


class TestNonFunctional:
    """Нефункциональные проверки"""

    @pytest.mark.nonfunctional
    def test_response_time_create_ad(self, base_url, valid_ad_data):
        """NF-001: Время ответа при создании объявления"""
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/1/item",
            json=valid_ad_data,
            headers={"Content-Type": "application/json"}
        )
        elapsed_time = time.time() - start_time

        assert response.status_code == 200
        assert elapsed_time < 2.0, f"Response time {elapsed_time:.2f}s exceeds 2s limit"

    @pytest.mark.nonfunctional
    def test_response_time_get_ad(self, base_url, created_ad):
        """NF-001: Время ответа при получении объявления"""
        ad_id = created_ad["id"]
        start_time = time.time()
        response = requests.get(
            f"{base_url}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        elapsed_time = time.time() - start_time

        assert response.status_code == 200
        assert elapsed_time < 2.0, f"Response time {elapsed_time:.2f}s exceeds 2s limit"

    @pytest.mark.security
    def test_sql_injection_in_name(self, base_url, random_seller_id):
        """NF-003: Проверка защиты от SQL инъекций"""
        sql_payloads = [
            "'; DROP TABLE items; --",
            "' OR '1'='1",
            "'; SELECT * FROM users; --"
        ]

        for payload in sql_payloads:
            ad_data = {
                "sellerId": random_seller_id,
                "name": payload,
                "price": 100
            }
            response = requests.post(
                f"{base_url}/api/1/item",
                json=ad_data,
                headers={"Content-Type": "application/json"}
            )

            assert response.status_code in [200, 400]

    @pytest.mark.security
    def test_xss_injection_in_name(self, base_url, random_seller_id):
        """NF-004: Проверка защиты от XSS"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]

        for payload in xss_payloads:
            ad_data = {
                "sellerId": random_seller_id,
                "name": payload,
                "price": 100
            }
            response = requests.post(
                f"{base_url}/api/1/item",
                json=ad_data,
                headers={"Content-Type": "application/json"}
            )

            assert response.status_code in [200, 400]