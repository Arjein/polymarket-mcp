import json
import pytest
from tests.conftest import mock_auth_clob, mcp_server
from tools.trading_tools import register_trading_tools

@pytest.mark.asyncio
async def test_place_order(mock_auth_clob, mcp_server):
    register_trading_tools(mcp_server, mock_auth_clob)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "place_order":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(token_id="123", price=0.5, size=10, side="BUY")
    
    # We returned {"orderID": "xyz123", "status": "posted"} from mock_auth_clob
    assert "xyz123" in result
    assert "posted" in result

@pytest.mark.asyncio
async def test_get_balance_allowance(mock_auth_clob, mcp_server):
    register_trading_tools(mcp_server, mock_auth_clob)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "get_balance_allowance":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func()
    
    assert "100.0" in result
    assert "1000.0" in result
