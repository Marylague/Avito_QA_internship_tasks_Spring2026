import pytest
import requests
import random

BASE_URL = "https://qa-internship.avito.com"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_seller_id():
    """Генерирует случайный sellerId в диапазоне 111111-999999"""
    return random.randint(111111, 999999)


@pytest.fixture
def valid_ad_data(random_seller_id):
    """Возвращает валидные данные для создания объявления"""
    return {
        "sellerID": random_seller_id,
        "name": f"Test Ad {random.randint(1, 10000)}",
        "price": random.randint(100, 100000),
        "likes": 0,  # при дебаге добавила сюда это поле
        "viewCount": 0,  # аналогично
        "contacts": 0  #  аналогично
    }


@pytest.fixture
def created_ad(valid_ad_data, base_url):
    """Создаёт объявление и возвращает его ID и данные"""
    response = requests.post(
        f"{base_url}/api/1/item",
        json=valid_ad_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"\nСоздание объявления:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")

    if response.status_code != 200:
        pytest.fail(f"Не удалось создать объявление. Статус: {response.status_code}, Ответ: {response.text}")

    response_data = response.json()

    status_text = response_data.get("status", "")
    ad_id = status_text.split(" - ")[-1] if " - " in status_text else None

    yield {
        "id": ad_id,
        "data": valid_ad_data,
        "full_data": response_data
    }

    # чистим
    if ad_id:
        try:
            requests.delete(f"{base_url}/api/2/item/{ad_id}")
        except:
            pass