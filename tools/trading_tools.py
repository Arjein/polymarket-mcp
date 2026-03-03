"""MCP tool registrations for authenticated Polymarket trading operations.

These tools allow the agent to place, cancel, and monitor orders on Polymarket.
Requires POLYMARKET_PRIVATE_KEY in .env. Set POLYMARKET_DRY_RUN=true for safe testing.
"""

from __future__ import annotations

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from clients.auth_clob import AuthenticatedClobClient


def register_trading_tools(mcp: FastMCP, auth_clob: AuthenticatedClobClient) -> None:
    """Register authenticated trading tools on the MCP server."""

    # ------------------------------------------------------------------
    # Order placement
    # ------------------------------------------------------------------

    @mcp.tool()
    async def place_order(
        token_id: str,
        price: float,
        size: float,
        side: str,
        order_type: Optional[str] = "GTC",
        tick_size: Optional[str] = "0.01",
        neg_risk: Optional[bool] = False,
    ) -> str:
        """Place a limit order on a Polymarket prediction market.

        ⚠️ WARNING: This action actively spends real currency! The total order value (price × size) is validated against the `POLYMARKET_MAX_ORDER_SIZE` prior to API submission.
        To test safely without financial execution, configure `POLYMARKET_DRY_RUN=true` in the environment `.env` file.

        Args:
            token_id (str): The fundamental CLOB token ID indicating the precise outcome side (e.g., YES or NO).
            price (float): The designated limit price, scaling strictly between 0.01 and 0.99 (representing outcome probability).
            size (float): The aggregate number of shares to purchase or sell.
            side (str): The functional trading direction, strictly either 'BUY' or 'SELL'.
            order_type (Optional[str]): The operational order type payload. Options: GTC (Good-Til-Cancelled), FOK (Fill-Or-Kill), GTD (Good-Til-Date), FAK (Fill-And-Kill).
            tick_size (Optional[str]): The calculated market tick size structure (e.g., '0.1', '0.01', '0.001', '0.0001').
            neg_risk (Optional[bool]): Designates whether the overarching market utilizes a negative risk framework.
        """
        result = auth_clob.place_order(
            token_id=token_id,
            price=price,
            size=size,
            side=side,
            order_type=order_type or "GTC",
            tick_size=tick_size or "0.01",
            neg_risk=neg_risk or False,
        )
        return json.dumps(result)

    @mcp.tool()
    async def cancel_order(order_id: str) -> str:
        """Cancel an individual specified open limit order directly via its unique ID.

        Args:
            order_id (str): The unique transaction order ID returned functionally during order placement.
        """
        result = auth_clob.cancel_order(order_id)
        return json.dumps(result)

    @mcp.tool()
    async def cancel_all_orders() -> str:
        """Cancel ALL currently active open orders sequentially. Functions as an emergency kill switch.

        Deploy this operation functionally to immediately liquidate all pending structural positions.
        """
        result = auth_clob.cancel_all_orders()
        return json.dumps(result)

    @mcp.tool()
    async def cancel_orders(order_ids: str) -> str:
        """Cancel multiple open limit orders concurrently via their unique IDs.

        Args:
            order_ids (str): A comma-separated sequential string of order IDs to be canceled.
        """
        ids = [oid.strip() for oid in order_ids.split(",")]
        result = auth_clob.cancel_orders(ids)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Order queries
    # ------------------------------------------------------------------

    @mcp.tool()
    async def get_open_orders(
        market: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> str:
        """Retrieve a comprehensive list of all open/pending limit orders currently active for the authenticated account.

        Args:
            market (Optional[str]): Explicitly filter results chronologically by market condition ID.
            asset_id (Optional[str]): Explicitly filter results specifically by CLOB token ID.
        """
        result = auth_clob.get_open_orders(market=market, asset_id=asset_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_order(order_id: str) -> str:
        """Retrieve granular structural details and fundamental status of a specifically defined order.

        Args:
            order_id (str): The unique transaction order ID to dynamically query.
        """
        result = auth_clob.get_order(order_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_balance_allowance(
        asset_type: Optional[str] = "COLLATERAL",
        token_id: Optional[str] = None,
    ) -> str:
        """Retrieve the functional token balance and structural approval threshold metrics on the Polymarket protocol.

        Args:
            asset_type (Optional[str]): 'COLLATERAL' to fetch the cumulative USDC balance or 'CONDITIONAL' to query conditional outcome token holdings.
            token_id (Optional[str]): Required intrinsically when the specified 'asset_type' functions as 'CONDITIONAL'.
        """
        result = auth_clob.get_balance_allowance(
            asset_type=asset_type or "COLLATERAL",
            token_id=token_id or None,
        )
        return json.dumps(result)
