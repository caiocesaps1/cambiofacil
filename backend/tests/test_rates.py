import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ("ok", "degraded", "unknown")
    assert data["cache"] in ("redis", "memory")
    assert "sources" in data


def test_get_rates_usd():
    res = client.get("/rates?currency=USD&amount=1000")
    assert res.status_code == 200
    data = res.json()
    assert data["currency"] == "USD"
    assert data["amount_brl"] == 1000.0
    assert len(data["rates"]) > 0
    # ordenado do melhor (maior amount_received) para o pior
    amounts = [r["amount_received"] for r in data["rates"]]
    assert amounts == sorted(amounts, reverse=True)


def test_get_rates_eur():
    res = client.get("/rates?currency=EUR&amount=2000")
    assert res.status_code == 200
    data = res.json()
    assert data["currency"] == "EUR"
    assert len(data["rates"]) > 0


def test_filter_by_type():
    res = client.get("/rates?currency=USD&amount=1000&type=fintech")
    assert res.status_code == 200
    data = res.json()
    for rate in data["rates"]:
        assert rate["type"] == "fintech"


def test_invalid_currency():
    res = client.get("/rates?currency=GBP&amount=1000")
    assert res.status_code == 422


def test_invalid_type():
    res = client.get("/rates?currency=USD&amount=1000&type=invalid")
    assert res.status_code == 400
