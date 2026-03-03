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
        """Retrieve historical price time-series data for a specified token.

        Provides a chronologically ordered list of objects containing timestamp and price data, facilitating charting and trend analysis.

        Args:
            token_id (str): The fundamental token ID associated with a specific outcome.
            interval (Optional[str]): A predefined time window ending at the current moment. Valid options include: '1h', '6h', '1d', '1w', '1m', 'max'. This parameter is mutually exclusive with 'start_ts'/'end_ts'.
            fidelity (Optional[int]): The data resolution expressed in minutes (e.g., 60 for hourly data, 1440 for daily data).
            start_ts (Optional[int]): The starting Unix timestamp in UTC. Use in conjunction with 'end_ts' instead of 'interval'.
            end_ts (Optional[int]): The ending Unix timestamp in UTC. Use in conjunction with 'start_ts' instead of 'interval'.
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
        """Retrieve the current open interest (total outstanding shares) for a specific market or globally.

        Open interest serves as an indicator of market conviction and overall liquidity.

        Args:
            condition_id (Optional[str]): The unique on-chain identifier for a specific market's conditions. Omit to retrieve a global aggregate.
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
        """Retrieve current portfolio positions and quantitative holdings for the authenticated user.

        Provides detailed position data including share size, average entry price, and calculated P&L for each held outcome token.
        Automatically utilizes the wallet address defined in the `POLYMARKET_WALLET_ADDRESS` environment variable.

        Args:
            market (Optional[str]): Filter results by a specific market condition ID.
            event_id (Optional[str]): Filter results by a specific overarching event ID.
            size_threshold (Optional[float]): The minimum numerical position size required for inclusion in the results.
            limit (Optional[int]): The maximum number of paginated results to return.
            offset (Optional[int]): The pagination offset.
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
        """Retrieve the historical log of executed trades associated with a specific user or market.

        Provides chronological records of executed trades, detailing transaction price, share size, designated side, and timestamp.

        Args:
            user (Optional[str]): The wallet address to query historical trades for.
            market (Optional[str]): Filter results by a specific market condition ID.
            limit (Optional[int]): The maximum number of paginated results to return.
            offset (Optional[int]): The pagination offset.
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
        """Retrieve a comprehensive activity log for the authenticated user, encompassing trades, splits, merges, and rewards.

        Provides a detailed audit trail of all supported account actions.
        Automatically utilizes the wallet address defined in the `POLYMARKET_WALLET_ADDRESS` environment variable.

        Args:
            market (Optional[str]): Filter logs by a specific market condition ID.
            activity_type (Optional[str]): Filter logs by explicit activity type (e.g., 'TRADE', 'SPLIT', 'MERGE', 'REDEEM', 'REWARD', 'CONVERSION').
            limit (Optional[int]): The maximum number of paginated results to return.
            offset (Optional[int]): The pagination offset.
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
