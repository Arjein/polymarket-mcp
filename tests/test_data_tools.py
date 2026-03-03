import json
import pytest
from tests.conftest import mock_data, mock_clob, mcp_server
from tools.data_tools import register_data_tools

@pytest.mark.asyncio
async def test_get_open_interest(mock_data, mock_clob, mcp_server):
    register_data_tools(mcp_server, mock_clob, mock_data)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "get_open_interest":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(condition_id="0x123")
    
    # We returned {"open_interest": 1000000} from mock_data
    assert "1000000" in result

@pytest.mark.asyncio
async def test_get_trade_history(mock_data, mock_clob, mcp_server):
    register_data_tools(mcp_server, mock_clob, mock_data)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "get_trade_history":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(user="0xabc")
    
    # We returned [{"price": 0.5, "size": 10}]
    assert "0.5" in result
    assert "10" in result
