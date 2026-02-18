"""MCP tool registrations for the Polymarket CLOB API."""

from __future__ import annotations

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from clients.clob import ClobClient


def register_clob_tools(mcp: FastMCP, clob: ClobClient) -> None:
    """Register all CLOB read-only tools on the MCP server."""

    # ------------------------------------------------------------------
    # Health & Meta
    # ------------------------------------------------------------------

    @mcp.tool()
    async def clob_health_check() -> str:
        """Check if the Polymarket CLOB API server is online and operational."""
        result = await clob.get_ok()
        return json.dumps(result) if not isinstance(result, str) else result

    @mcp.tool()
    async def clob_server_time() -> str:
        """Get the current Polymarket CLOB server timestamp."""
        result = await clob.get_server_time()
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_clob_markets(next_cursor: Optional[str] = None) -> str:
        """Get a paginated list of all markets on the Polymarket CLOB.

        Returns market data including condition IDs, token IDs, and trading parameters.
        Use next_cursor from a previous response to paginate through results.

        Args:
            next_cursor: Pagination cursor from a previous response. Omit for the first page.
        """
        result = await clob.get_markets(next_cursor=next_cursor or "MA==")
        return json.dumps(result)

    @mcp.tool()
    async def get_clob_simplified_markets(next_cursor: Optional[str] = None) -> str:
        """Get a paginated compact list of CLOB markets (less detail, faster).

        Args:
            next_cursor: Pagination cursor. Omit for the first page.
        """
        result = await clob.get_simplified_markets(next_cursor=next_cursor or "MA==")
        return json.dumps(result)

    @mcp.tool()
    async def get_clob_market(condition_id: str) -> str:
        """Get detailed information about a single CLOB market.

        Args:
            condition_id: The on-chain condition ID of the market.
        """
        result = await clob.get_market(condition_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_market_trades_events(condition_id: str) -> str:
        """Get live trade activity/events for a specific market.

        Args:
            condition_id: The on-chain condition ID of the market.
        """
        result = await clob.get_market_trades_events(condition_id)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Order Book
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_order_book(token_id: str) -> str:
        """Get the full order book (bids and asks) for a specific outcome token.

        The order book shows all open buy and sell orders at each price level.

        Args:
            token_id: The CLOB token ID for the outcome (YES or NO side of a market).
        """
        result = await clob.get_order_book(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_order_books(token_ids: str) -> str:
        """Get order books for multiple tokens at once.

        Args:
            token_ids: Comma-separated list of CLOB token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_order_books(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Prices
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_price(token_id: str, side: str) -> str:
        """Get the current best price for a token on a given side.

        The price represents the probability of the outcome (0.00 to 1.00).

        Args:
            token_id: The CLOB token ID for the outcome.
            side: Either "BUY" or "SELL".
        """
        result = await clob.get_price(token_id, side)
        return json.dumps(result)

    @mcp.tool()
    async def get_midpoint(token_id: str) -> str:
        """Get the mid-market price for a token.

        The midpoint is the average of the best bid and best ask prices.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_midpoint(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_midpoints(token_ids: str) -> str:
        """Get mid-market prices for multiple tokens at once.

        Args:
            token_ids: Comma-separated list of CLOB token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_midpoints(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Spreads
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_spread(token_id: str) -> str:
        """Get the bid-ask spread for a token.

        The spread indicates market liquidity — smaller spreads mean more liquid markets.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_spread(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_spreads(token_ids: str) -> str:
        """Get bid-ask spreads for multiple tokens at once.

        Args:
            token_ids: Comma-separated list of CLOB token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_spreads(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Last Trade Prices
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_last_trade_price(token_id: str) -> str:
        """Get the price at which the last trade was executed for a token.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_last_trade_price(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_last_trades_prices(token_ids: str) -> str:
        """Get last trade prices for multiple tokens at once.

        Args:
            token_ids: Comma-separated list of CLOB token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_last_trades_prices(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Market Metadata
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_tick_size(token_id: str) -> str:
        """Get the minimum tick size (price increment) for a token's market.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_tick_size(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_neg_risk(token_id: str) -> str:
        """Check whether a token's market uses negative risk.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_neg_risk(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_fee_rate(token_id: str) -> str:
        """Get the trading fee rate (in basis points) for a token's market.

        Args:
            token_id: The CLOB token ID for the outcome.
        """
        result = await clob.get_fee_rate(token_id)
        return json.dumps(result)
