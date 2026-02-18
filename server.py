"""Polymarket MCP Server – Full trading agent toolkit.

Exposes Polymarket's CLOB, Gamma, and Data API data as MCP tools
for use by LLM agents. Includes authenticated order management.
"""

from mcp.server.fastmcp import FastMCP

from clients.auth_clob import AuthenticatedClobClient
from clients.clob import ClobClient
from clients.data import DataClient
from clients.gamma import GammaClient
from tools.clob_tools import register_clob_tools
from tools.data_tools import register_data_tools
from tools.gamma_tools import register_gamma_tools
from tools.trading_tools import register_trading_tools

# ---------------------------------------------------------------------------
# Instantiate clients
# ---------------------------------------------------------------------------

clob = ClobClient()
data = DataClient()
gamma = GammaClient()
auth_clob = AuthenticatedClobClient()

# ---------------------------------------------------------------------------
# Create MCP server and register tools
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "polymarket",
    instructions=(
        "Polymarket MCP server providing full access to prediction market data and trading. "
        "Use the Gamma tools (search_events, search_markets) to discover markets, "
        "then use CLOB tools (get_price, get_order_book, get_midpoint, etc.) to "
        "retrieve real-time trading data using the token IDs from the Gamma results. "
        "Use get_price_history for trend analysis and get_open_interest for conviction signals. "
        "Use get_positions, get_trade_history, and get_activity for account monitoring. "
        "Use place_order, cancel_order, etc. for trading (requires API credentials in .env)."
    ),
)

register_clob_tools(mcp, clob)
register_data_tools(mcp, clob, data)
register_gamma_tools(mcp, gamma)
register_trading_tools(mcp, auth_clob)

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")

