import pytest
from tests.conftest import mock_clob, mcp_server
from tools.clob_tools import register_clob_tools

@pytest.mark.asyncio
async def test_clob_health_check(mock_clob, mcp_server):
    register_clob_tools(mcp_server, mock_clob)
    
    # We retrieve the actual function wrapped by the FastMCP tool wrapper.
    # We must access the original method since FastMCP doesn't intrinsically provide async execution context easily
    
    # Alternatively we can simulate the tool calls
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "clob_health_check":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func()
    assert result == "OK"

@pytest.mark.asyncio
async def test_get_clob_markets(mock_clob, mcp_server):
    register_clob_tools(mcp_server, mock_clob)
    
    tool_func = None
    tools = mcp_server._tool_manager.list_tools()
    for tool in tools:
        if tool.name == "get_clob_markets":
            tool_func = tool.fn
            break
            
    assert tool_func is not None
    result = await tool_func(next_cursor="MA==")
    
    assert "0x123" in result
    assert "Will X happen?" in result
