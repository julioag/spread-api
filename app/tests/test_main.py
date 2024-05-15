from fastapi.testclient import TestClient

from app.main import api

client = TestClient(api)


def test_get_market_spread():
    response = client.get("/spread/btc-clp")
    assert response.status_code == 200
    data = response.json()
    assert list(data.keys())[0] == "spread"
    assert type(list(data.values())[0]) == float


def test_get_all_market_spreads():
    response = client.get("/spread")
    assert response.status_code == 200
    data = response.json()
    assert type(data) is dict


def test_post_new_spread_alert():
    response = client.post("/spread-alert/", json={"market": "btc-clp", "spread": 100})
    assert response.status_code == 201
    data = response.json()
    assert data["market"] == "btc-clp"
    assert data["spread"] == 100.0
    response2 = client.get("/spread-alert/btc-clp")
    assert response2.status_code == 200
    data2 = response2.json()
    assert list(data2.keys())[0] == "spread"
    assert type(list(data2.values())[0]) == float
    assert data2.get("spread") == 100.0


def test_compare_spread_alerts():
    response = client.post("/spread-alert/", json={"market": "btc-clp", "spread": 100})
    assert response.status_code == 201
    response = client.get(
        "/compare-spread-alert", params={"market_id": "btc-clp", "spread": 100}
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("alert") == "spread is equal to the alert"
    response2 = client.get("/compare-spread-alert?market_id=btc-clp&spread=50")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2.get("alert") == "spread is lower than the alert"
    response3 = client.get("/compare-spread-alert?market_id=btc-clp&spread=100")
    assert response3.status_code == 200
    data3 = response3.json()
    assert data3.get("alert") == "spread is equal to the alert"
    response4 = client.get("/compare-spread-alert?market_id=btc-clp&spread=100.0")
    assert response4.status_code == 200
    data4 = response4.json()
    assert data4.get("alert") == "spread is equal to the alert"
    response5 = client.get("/compare-spread-alert?market_id=btc-clp&spread=100.1")
    assert response5.status_code == 200
    data5 = response5.json()
    assert data5.get("alert") == "spread is higher than the alert"
