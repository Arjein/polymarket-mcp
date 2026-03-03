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
        """Check if the Polymarket Central Limit Order Book (CLOB) API server is reachable and operational.
        Returns 'OK' if the API is currently healthy."""
        result = await clob.get_ok()
        return json.dumps(result) if not isinstance(result, str) else result

    @mcp.tool()
    async def clob_server_time() -> str:
        """Get the current server time from the Polymarket CLOB API as a Unix timestamp."""
        result = await clob.get_server_time()
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_clob_markets(next_cursor: Optional[str] = None) -> str:
        """Retrieve a paginated list of all prediction markets actively trading on the Polymarket CLOB API.

        Provides comprehensive details for each market, including the on-chain condition IDs, corresponding outcome token IDs, and trading configuration parameters.

        Args:
            next_cursor (Optional[str]): The pagination cursor string returned from a previous request. Omit this argument to fetch the first page of results.
        """
        result = await clob.get_markets(next_cursor=next_cursor or "MA==")
        return json.dumps(result)

    @mcp.tool()
    async def get_clob_simplified_markets(next_cursor: Optional[str] = None) -> str:
        """Retrieve a paginated, simplified list of all prediction markets actively trading on the Polymarket CLOB API.

        This provides less detail than get_clob_markets but operates significantly faster, making it suitable for overview data.

        Args:
            next_cursor (Optional[str]): The pagination cursor string returned from a previous request. Omit this argument to fetch the first page of results.
        """
        result = await clob.get_simplified_markets(next_cursor=next_cursor or "MA==")
        return json.dumps(result)

    @mcp.tool()
    async def get_clob_market(condition_id: str) -> str:
        """Retrieve detailed, comprehensive information regarding a single Polymarket prediction market.

        Args:
            condition_id (str): The unique on-chain identifier corresponding to the specific market's conditions.
        """
        result = await clob.get_market(condition_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_market_trades_events(condition_id: str) -> str:
        """Fetch the stream of live trade activity and lifecycle events occurring on a specific Polymarket prediction market.

        Args:
            condition_id (str): The unique on-chain identifier corresponding to the specific market's conditions.
        """
        result = await clob.get_market_trades_events(condition_id)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Order Book
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_order_book(token_id: str) -> str:
        """Retrieve the current full depth of the order book (all pending bids and asks) for a specific outcome token.

        This provides a complete snapshot of all open buy and sell orders mapped to their respective price levels.

        Args:
            token_id (str): The fundamental token ID associated with a specific outcome (e.g., the YES or NO side of the bet) in a prediction market.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_order_book(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_order_books(token_ids: str) -> str:
        """Retrieve the current order books for up to multiple discrete tokens concurrently.

        Args:
            token_ids (str): A comma-separated list of foundational token IDs to fetch mapping for.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_order_books(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Prices
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_price(token_id: str, side: str) -> str:
        """Fetch the single best available price for a given outcome token on a specified directional side.

        Pricing maps intrinsically to outcome probabilities in the range `0.00` to `1.00`.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
            side (str): The designated trading side to check, either strictly 'BUY' or 'SELL'.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_price(token_id, side)
        return json.dumps(result)

    @mcp.tool()
    async def get_midpoint(token_id: str) -> str:
        """Calculate and return the mid-market price for a specified outcome token.

        The midpoint serves as a fair-value indicator generated by averaging the current best bid and best ask prices.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_midpoint(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_midpoints(token_ids: str) -> str:
        """Calculate and return the mid-market prices concurrently for multiple outcome tokens.

        Args:
            token_ids (str): A comma-separated list of foundational token IDs to fetch fair value for.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_midpoints(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Spreads
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_spread(token_id: str) -> str:
        """Calculate and return the current bid-ask spread for a specified outcome token.

        The spread serves as a key liquidity indicator; smaller spreads typically denote deeper, more efficient markets.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_spread(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_spreads(token_ids: str) -> str:
        """Calculate and return the current bid-ask spreads for multiple specified tokens concurrently.

        Args:
            token_ids (str): A comma-separated list of foundational token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_spreads(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Last Trade Prices
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_last_trade_price(token_id: str) -> str:
        """Retrieve the exact transaction price of the most recently executed trade for an outcome token.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_last_trade_price(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_last_trades_prices(token_ids: str) -> str:
        """Retrieve the transaction prices of the most recently executed trades for multiple outcome tokens concurrently.

        Args:
            token_ids (str): A comma-separated list of foundational token IDs.
        """
        ids = [tid.strip() for tid in token_ids.split(",")]
        result = await clob.get_last_trades_prices(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Market Metadata
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_tick_size(token_id: str) -> str:
        """Retrieve the minimum allowable price increment (tick size) for trading a specific token's market.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_tick_size(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_neg_risk(token_id: str) -> str:
        """Verify whether a specified outcome token's market utilizes the negative risk mathematical framework.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_neg_risk(token_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_fee_rate(token_id: str) -> str:
        """Retrieve the baseline trading fee rate (measured in basis points) applicable to a specific token's market.

        Args:
            token_id (str): The fundamental token identifier indicating the outcome side.
        """
        if not token_id:
            return json.dumps({"error": "token_id is required"})
        result = await clob.get_fee_rate(token_id)
        return json.dumps(result)
