"""Модуль 10. Code review тестов.

Это PR джуна в api_tests/. Тесты «зелёные у автора». Сделай ревью, как в реальной команде:
найди проблемы, для каждой — строка, почему плохо, как исправить, и важность (blocker / major / minor / nit).
Ответы пиши внизу файла, в блоке ОТВЕТЫ. Проблем больше 15.
"""

import time
import random
import requests

URL = "http://localhost:8080"
token = None
order_id = None


def test_1():
    global token
    r = requests.post(URL + "/auth/register", json={"email": "trader@test.io", "password": "password123"})
    r = requests.post(URL + "/auth/login", json={"email": "trader@test.io", "password": "password123"})
    token = r.json()["access_token"]
    print(token)


def test_2():
    global order_id
    h = {"Authorization": "Bearer " + token}
    requests.post(URL + "/balances/deposit", json={"asset": "USDT", "amount": 100}, headers=h)
    r = requests.post(URL + "/orders", json={
        "symbol": "ETH-USDT", "side": "BUY", "price": str(random.randint(1, 50)), "quantity": "1"
    }, headers=h)
    order_id = r.json()["id"]
    assert r.status_code == 201 or r.status_code == 200


def test_balance_after_order():
    h = {"Authorization": "Bearer " + token}
    r = requests.get(URL + "/balances", headers=h)
    usdt = [b for b in r.json() if b["asset"] == "USDT"][0]
    assert float(usdt["available"]) + float(usdt["locked"]) == 100.0


def test_trade():
    h = {"Authorization": "Bearer " + token}
    requests.post(URL + "/orders", json={
        "symbol": "ETH-USDT", "side": "SELL", "price": "1", "quantity": "1"
    }, headers=h)
    time.sleep(3)
    r = requests.get(URL + "/orders/" + order_id, headers=h)
    try:
        assert r.json()["status"] == "FILLED"
    except Exception:
        pass


def test_cancel():
    h = {"Authorization": "Bearer " + token}
    r = requests.delete(URL + "/orders/" + order_id, headers=h)
    assert r.status_code < 500
    if r.status_code == 200:
        assert r.json()["status"] == "CANCELED"


def test_everything_about_orders():
    h = {"Authorization": "Bearer " + token}
    for price in ["0", "-1", "abc", "1"]:
        r = requests.post(URL + "/orders", json={
            "symbol": "ETH-USDT", "side": "BUY", "price": price, "quantity": "1"
        }, headers=h)
        if price == "1":
            assert r.status_code == 201
        else:
            assert r.status_code == 422
    r = requests.get(URL + "/orders", headers=h)
    assert len(r.json()) == 3


# ОТВЕТЫ (строка — проблема — почему — как исправить — важность):
#
