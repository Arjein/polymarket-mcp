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
        """Place a limit order on a Polymarket market.

        ⚠️ This spends real money! The order value (price × size) is
        checked against POLYMARKET_MAX_ORDER_SIZE before submission.
        Set POLYMARKET_DRY_RUN=true in .env to simulate without executing.

        Args:
            token_id: The CLOB token ID for the outcome (YES or NO side).
            price: Limit price between 0.01 and 0.99 (probability).
            size: Number of shares to buy/sell.
            side: "BUY" or "SELL".
            order_type: Order type. GTC (Good-Til-Cancelled, default),
                        FOK (Fill-Or-Kill), GTD (Good-Til-Date),
                        FAK (Fill-And-Kill).
            tick_size: Market tick size ("0.1", "0.01", "0.001", "0.0001").
            neg_risk: Whether the market uses negative risk.
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
        """Cancel a specific open order by its ID.

        Args:
            order_id: The order ID returned when the order was placed.
        """
        result = auth_clob.cancel_order(order_id)
        return json.dumps(result)

    @mcp.tool()
    async def cancel_all_orders() -> str:
        """Cancel ALL open orders. Emergency kill switch.

        Use this to immediately exit all pending positions.
        """
        result = auth_clob.cancel_all_orders()
        return json.dumps(result)

    @mcp.tool()
    async def cancel_orders(order_ids: str) -> str:
        """Cancel multiple orders by their IDs.

        Args:
            order_ids: Comma-separated list of order IDs to cancel.
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
        """Get all open/pending orders for your account.

        Args:
            market: Filter by market condition ID.
            asset_id: Filter by specific token ID.
        """
        result = auth_clob.get_open_orders(market=market, asset_id=asset_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_order(order_id: str) -> str:
        """Get details and status of a specific order.

        Args:
            order_id: The order ID to look up.
        """
        result = auth_clob.get_order(order_id)
        return json.dumps(result)

    @mcp.tool()
    async def get_balance_allowance(
        asset_type: Optional[str] = "COLLATERAL",
        token_id: Optional[str] = "",
    ) -> str:
        """Get your USDC balance and approval status on Polymarket.

        Args:
            asset_type: "COLLATERAL" for USDC balance, "CONDITIONAL" for
                        outcome token balance (requires token_id).
            token_id: Required when asset_type is CONDITIONAL.
        """
        result = auth_clob.get_balance_allowance(
            asset_type=asset_type or "COLLATERAL",
            token_id=token_id or "",
        )
        return json.dumps(result)
