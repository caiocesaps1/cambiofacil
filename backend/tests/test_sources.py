import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.rate import Currency
from app.services.sources.wise import WiseSource
from app.services.sources.nomad import NomadSource
from app.services.sources.confidence import ConfidenceSource


# ---------------------------------------------------------------------------
# Wise
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_wise_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = [{"rate": 0.1718}]  # 1 BRL = 0.1718 USD → 1 USD = ~5.82 BRL

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "Wise"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == round(1 / 0.1718, 4)
    assert rate.spread_pct >= 0


@pytest.mark.asyncio
async def test_wise_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("timeout"))
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None


@pytest.mark.asyncio
async def test_wise_returns_none_on_empty_response():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = []

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None


# ---------------------------------------------------------------------------
# Nomad
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_nomad_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = [
        {"currency": "USD", "buy": "5.85", "sell": "5.75"},
        {"currency": "EUR", "buy": "6.30", "sell": "6.20"},
    ]

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "Nomad"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == 5.85
    assert rate.sell_rate == 5.75


@pytest.mark.asyncio
async def test_nomad_returns_none_when_currency_not_found():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = [{"currency": "EUR", "buy": "6.30", "sell": "6.20"}]

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None


@pytest.mark.asyncio
async def test_nomad_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("connection error"))
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.EUR)

    assert rate is None


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------

CONFIDENCE_HTML_USD = """
<html><body>
  <div data-currency="dolar">
    <span data-type="buy">5,92</span>
    <span data-type="sell">5,80</span>
  </div>
</body></html>
"""

CONFIDENCE_HTML_EUR = """
<html><body>
  <div data-currency="euro">
    <span data-type="buy">6,40</span>
    <span data-type="sell">6,28</span>
  </div>
</body></html>
"""


@pytest.mark.asyncio
async def test_confidence_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.text = CONFIDENCE_HTML_USD

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "Confidence"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == 5.92
    assert rate.sell_rate == 5.80


@pytest.mark.asyncio
async def test_confidence_eur_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.text = CONFIDENCE_HTML_EUR

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.EUR)

    assert rate is not None
    assert rate.buy_rate == 6.40
    assert rate.sell_rate == 6.28


@pytest.mark.asyncio
async def test_confidence_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("timeout"))
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None
