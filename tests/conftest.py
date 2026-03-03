import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_clob():
    """Mock the ClobClient."""
    mock = AsyncMock()
    # Health checks
    mock.get_ok.return_value = "OK"
    mock.get_server_time.return_value = "1700000000"
    
    # Markets
    mock.get_markets.return_value = {"data": [{"condition_id": "0x123", "market": "Will X happen?"}], "next_cursor": "MA=="}
    mock.get_simplified_markets.return_value = {"data": [{"condition_id": "0x123"}], "next_cursor": "MA=="}
    mock.get_market.return_value = {"condition_id": "0x123", "question": "Will X happen?"}
    mock.get_market_trades_events.return_value = [{"price": 0.5, "size": 100}]

    # Prices and orderbook
    mock.get_price.return_value = {"price": 0.5}
    mock.get_midpoint.return_value = {"mid": 0.55}
    mock.get_spread.return_value = {"spread": 0.02}
    mock.get_tick_size.return_value = {"tick_size": 0.01}
    mock.get_neg_risk.return_value = {"negative_risk": False}
    
    return mock

@pytest.fixture
def mock_data():
    """Mock DataClient."""
    mock = AsyncMock()
    mock.get_open_interest.return_value = {"open_interest": 1000000}
    mock.get_positions.return_value = [{"market": "0x123", "size": 100, "entry_price": 0.4}]
    mock.get_trades.return_value = [{"price": 0.5, "size": 10}]
    mock.get_activity.return_value = [{"type": "TRADE", "details": "bought 10 yes"}]
    return mock

@pytest.fixture
def mock_gamma():
    """Mock GammaClient."""
    mock = AsyncMock()
    mock.get_events.return_value = [{"id": "1", "title": "Election 2024"}]
    mock.get_event.return_value = {"id": "1", "title": "Election 2024", "markets": []}
    mock.get_markets.return_value = [{"id": "10", "question": "Will X win?"}]
    mock.get_market.return_value = {"id": "10", "question": "Will X win?"}
    return mock

@pytest.fixture
def mock_auth_clob():
    """Mock AuthenticatedClobClient."""
    mock = MagicMock()
    mock.place_order.return_value = {"orderID": "xyz123", "status": "posted"}
    mock.cancel_order.return_value = {"status": "canceled"}
    mock.cancel_all_orders.return_value = [{"status": "canceled"}]
    mock.get_open_orders.return_value = [{"orderID": "xyz123", "price": 0.5}]
    mock.get_balance_allowance.return_value = {"balance": 100.0, "allowance": 1000.0}
    return mock

@pytest.fixture
def mcp_server():
    """Mock FastMCP server to register tools."""
    from mcp.server.fastmcp import FastMCP
    return FastMCP("TestServer")
