# Avito_QA_internship_tasks_Spring2026

# API Тестирование микросервиса объявлений

## Описание
Автоматизированные тесты для API микросервиса объявлений Avito.
Из дополнительных затрагивала E2E-тестирование

### Эндпоинты:
- `POST /api/1/item` - Создание объявления
- `GET /api/1/item/:id` - Получение объявления по ID
- `GET /api/1/:sellerID/item` - Получение объявлений продавца
- `GET /api/1/statistic/:id` - Получение статистики (v1)
- `GET /api/2/statistic/:id` - Получение статистики (v2)
- `DELETE /api/2/item/:id` - Удаление объявления

## Требования
- Python 3.8+
- pip

## Установка

1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd avito-api-tests
```
2. Создание виртуального окружения (рекомендуется)
``` bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```
3. Установка зависимостей
``` bash
pip install -r requirements.txt
```
4. Проверка установки
```bash
pytest --version
```
5. Запуск тестов
Запуск всех тестов
``` bash
pytest -v
```
Запуск с подробным выводом
``` bash
bash
pytest -v -s
```