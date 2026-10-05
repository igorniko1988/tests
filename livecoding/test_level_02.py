"""
1. Описать тест-кейсы / чек-лист для указанного эндпоинта.
2. Реализовать API-тесты на Python (requests + pytest): сначала самый важный кейс,
   затем остальные — сколько успеешь.

Test cases for GET /v1/catalog endpoint.

API Documentation:
- URL: http://localhost:8090/v1/catalog
- Method: GET
- Query parameters (все необязательные, можно комбинировать):
    - category: str — electronics | clothes | books | home
    - min_price: float, >= 0 — цена от (включительно)
    - max_price: float, >= 0 — цена до (включительно)
    - in_stock: bool — true | false
- Response 200:
    {
        "count": int,                 # сколько товаров в items
        "items": [
            {
                "id": int,
                "name": str,
                "category": str,      # electronics | clothes | books | home
                "price": float,       # > 0
                "in_stock": bool,
            },
        ]
    }
- Без фильтров возвращается весь каталог (12 товаров).
- Если ничего не подошло: {"count": 0, "items": []}
- Response 400 (невалидное значение фильтра или min_price > max_price):
    {"error": "bad_request"}
"""

# --- Уточняющие вопросы ---
# 1. Границы min_price / max_price включительно? (в документации — да)
# 2. Фильтры комбинируются через «И»? Можно передать несколько категорий сразу?
# 3. Неизвестный параметр (?color=red) игнорируется или даёт 400? Регистр категории важен?
# 4. Есть пагинация/лимит? Гарантирован ли порядок товаров?
# 5. Каталог стабилен — можно опираться на конкретные товары и цены?
# 6. Нужна авторизация? Есть ли SLA по времени ответа?

# --- Чек-лист ---
# P0 Позитивные:
#   1. Без фильтров → 200, 12 товаров, схема, count == len(items)
#   2. Каждая категория → все товары из неё И ни один товар этой категории не потерян
# P1 Цена (границы включительно):
#   3. Диапазон → все цены внутри, подходящие не потеряны
#   4. min_price = цена товара → товар в выдаче; max_price = цена товара → товар в выдаче
#   5. min_price = max_price → ровно товары с этой ценой
#   6. min_price=0 → весь каталог
# P1 Наличие:
#   7. in_stock=true / false → только товары с таким признаком
# P1 Комбинации:
#   8. category + in_stock + диапазон цен — все условия одновременно
# P1 Пустой результат:
#   9. min_price=100000 → {"count": 0, "items": []}
# P1 Невалидные → 400 {"error": "bad_request"}:
#  10. category=food, category=Books, min_price=-1, min_price=abc, in_stock=maybe
#  11. min_price > max_price
# P3 Проговорить: неизвестный параметр, время ответа, 405 на POST

# --- Самый важный кейс и почему ---
# Фильтр возвращает только подходящие товары и все подходящие (точность + полнота).
# Ради этого эндпоинт существует: иначе пользователь не найдёт товар или увидит лишнее.

# --- Тесты ---
from typing import Literal

import pytest
import requests
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr

BASE_URL = "http://localhost:8090/v1/catalog"
CATEGORIES = ["electronics", "clothes", "books", "home"]


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: StrictInt
    name: StrictStr = Field(min_length=1)
    category: Literal["electronics", "clothes", "books", "home"]
    price: StrictFloat = Field(gt=0)
    in_stock: StrictBool


class CatalogResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: StrictInt
    items: list[Product]


def search(**filters):
    return requests.get(BASE_URL, params=filters, timeout=10)


def get_catalog(**filters) -> CatalogResponse:
    """Запрос + проверка статуса и схемы — общая часть всех позитивных тестов."""
    response = search(**filters)
    assert response.status_code == 200
    catalog = CatalogResponse.model_validate(response.json())
    assert catalog.count == len(catalog.items)
    return catalog


def ids(products) -> set[int]:
    return {product.id for product in products}


@pytest.fixture(scope="module")
def full_catalog() -> list[Product]:
    """Весь каталог без фильтров — эталон, с которым сравниваем отфильтрованные выдачи."""
    return get_catalog().items


# P0
def test_without_filters_returns_whole_catalog():
    catalog = get_catalog()

    assert catalog.count == 12


@pytest.mark.parametrize("category", CATEGORIES)
def test_filter_by_category(category, full_catalog):
    catalog = get_catalog(category=category)

    expected = {p.id for p in full_catalog if p.category == category}
    assert expected  # в категории есть товары — иначе проверка ниже ничего не значит
    assert ids(catalog.items) == expected  # только подходящие и все подходящие


# P1 — цена
@pytest.mark.parametrize(("min_price", "max_price"), [(10, 50), (0, 20), (100, 1000)])
def test_filter_by_price_range(min_price, max_price, full_catalog):
    catalog = get_catalog(min_price=min_price, max_price=max_price)

    expected = {p.id for p in full_catalog if min_price <= p.price <= max_price}
    assert ids(catalog.items) == expected


def test_price_boundaries_are_inclusive():
    # Atlas (id 9) и Lamp (id 11) стоят ровно 45.0
    assert {9, 11} <= ids(get_catalog(min_price=45.0).items)
    assert {9, 11} <= ids(get_catalog(max_price=45.0).items)
    assert ids(get_catalog(min_price=45.0, max_price=45.0).items) == {9, 11}


def test_min_price_zero_returns_whole_catalog(full_catalog):
    assert ids(get_catalog(min_price=0).items) == ids(full_catalog)


# P1 — наличие
@pytest.mark.parametrize("in_stock", [True, False])
def test_filter_by_stock(in_stock, full_catalog):
    catalog = get_catalog(in_stock=str(in_stock).lower())

    expected = {p.id for p in full_catalog if p.in_stock is in_stock}
    assert ids(catalog.items) == expected


# P1 — комбинация
def test_filters_are_combined(full_catalog):
    catalog = get_catalog(category="electronics", in_stock="true", min_price=50, max_price=1000)

    expected = {
        p.id
        for p in full_catalog
        if p.category == "electronics" and p.in_stock and 50 <= p.price <= 1000
    }
    assert ids(catalog.items) == expected


# P1 — пустой результат
def test_nothing_found_returns_empty_list():
    response = search(min_price=100000)

    assert response.status_code == 200
    assert response.json() == {"count": 0, "items": []}


# P1 — невалидные
@pytest.mark.parametrize(
    "filters",
    [
        {"category": "food"},
        {"category": "Books"},
        {"min_price": -1},
        {"min_price": "abc"},
        {"in_stock": "maybe"},
        {"min_price": 100, "max_price": 10},
    ],
    ids=["unknown-category", "wrong-case", "negative-price", "not-a-number", "bad-bool", "min>max"],
)
def test_invalid_filters_return_400(filters):
    response = search(**filters)

    assert response.status_code == 400
    assert response.json() == {"error": "bad_request"}
