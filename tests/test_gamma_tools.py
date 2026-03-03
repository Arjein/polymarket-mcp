import json
import pytest
from tests.conftest import mock_gamma, mcp_server
from tools.gamma_tools import register_gamma_tools

@pytest.mark.asyncio
async def test_search_events(mock_gamma, mcp_server):
    register_gamma_tools(mcp_server, mock_gamma)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "search_events":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(query="Election")
    
    # We returned a mock list from mock_gamma
    assert "Election 2024" in result

@pytest.mark.asyncio
async def test_search_markets(mock_gamma, mcp_server):
    register_gamma_tools(mcp_server, mock_gamma)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "search_markets":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(query="Will X win?")
    
    assert "Will X win?" in result
