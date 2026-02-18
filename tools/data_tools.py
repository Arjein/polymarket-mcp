"""MCP tool registrations for the Polymarket Data API + CLOB price history."""

from __future__ import annotations

import json
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

from clients.clob import ClobClient
from clients.data import DataClient


def register_data_tools(mcp: FastMCP, clob: ClobClient, data: DataClient) -> None:
    """Register analytics and account-data tools on the MCP server."""

    # ------------------------------------------------------------------
    # Phase 2a – Analytics (public, no auth)
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_price_history(
        token_id: str,
        interval: Optional[str] = None,
        fidelity: Optional[int] = None,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
    ) -> str:
        """Get historical price time-series for a token.

        Returns a list of {t, p} objects (timestamp, price) for charting
        and trend analysis. Essential for identifying momentum and reversals.

        Args:
            token_id: The CLOB token ID for the outcome.
            interval: Preset window ending now. One of: 1h, 6h, 1d, 1w, 1m, max.
                      Mutually exclusive with start_ts/end_ts.
            fidelity: Data resolution in minutes (e.g. 60 for hourly, 1440 for daily).
            start_ts: Start unix timestamp (UTC). Use with end_ts instead of interval.
            end_ts: End unix timestamp (UTC). Use with start_ts instead of interval.
        """
        result = await clob.get_prices_history(
            token_id,
            interval=interval,
            fidelity=fidelity,
            start_ts=start_ts,
            end_ts=end_ts,
        )
        return json.dumps(result)

    @mcp.tool()
    async def get_open_interest(
        condition_id: Optional[str] = None,
    ) -> str:
        """Get open interest (total shares outstanding) for a market.

        High open interest indicates strong market conviction and liquidity.
        Compare with volume to gauge whether new money is entering the market.

        Args:
            condition_id: The on-chain condition ID. Omit for global aggregate.
        """
        result = await data.get_open_interest(condition_id=condition_id)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Phase 2b – Account data (may require wallet address)
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_positions(
        market: Optional[str] = None,
        event_id: Optional[str] = None,
        size_threshold: Optional[float] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """Get your current positions / holdings.

        Returns position data including size, average entry price, and P&L
        for each outcome token you hold. Uses POLYMARKET_WALLET_ADDRESS from .env.

        Args:
            market: Filter by market condition ID.
            event_id: Filter by event ID.
            size_threshold: Minimum position size to include.
            limit: Maximum number of results.
            offset: Pagination offset.
        """
        user = os.getenv("POLYMARKET_WALLET_ADDRESS")
        if not user:
            return json.dumps({"error": "POLYMARKET_WALLET_ADDRESS not set in .env"})
        result = await data.get_positions(
            user=user,
            market=market,
            event_id=event_id,
            size_threshold=size_threshold,
            limit=limit,
            offset=offset,
        )
        return json.dumps(result)

    @mcp.tool()
    async def get_trade_history(
        user: Optional[str] = None,
        market: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """Get historical trades for a user or market.

        Returns executed trade records with price, size, side, and timestamp.

        Args:
            user: Wallet address to query trades for.
            market: Filter by market condition ID.
            limit: Maximum number of results.
            offset: Pagination offset.
        """
        result = await data.get_trades(
            user=user,
            market=market,
            limit=limit,
            offset=offset,
        )
        return json.dumps(result)

    @mcp.tool()
    async def get_activity(
        market: Optional[str] = None,
        activity_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """Get your activity log (trades, splits, merges, rewards).

        Provides a complete audit trail of all account activity.
        Uses POLYMARKET_WALLET_ADDRESS from .env.

        Args:
            market: Filter by market condition ID.
            activity_type: Filter by type: TRADE, SPLIT, MERGE, REDEEM, REWARD, CONVERSION.
            limit: Maximum number of results.
            offset: Pagination offset.
        """
        user = os.getenv("POLYMARKET_WALLET_ADDRESS")
        if not user:
            return json.dumps({"error": "POLYMARKET_WALLET_ADDRESS not set in .env"})
        result = await data.get_activity(
            user=user,
            market=market,
            activity_type=activity_type,
            limit=limit,
            offset=offset,
        )
        return json.dumps(result)
