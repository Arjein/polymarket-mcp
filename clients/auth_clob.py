"""Authenticated wrapper around the py-clob-client for order management.

Uses the official py-clob-client library for signing and submitting orders.
Requires POLYMARKET_PRIVATE_KEY (and optionally API credentials) in .env.

This client is SEPARATE from the lightweight ClobClient used for public reads.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Chain ID for Polygon mainnet
POLYGON_CHAIN_ID = 137
CLOB_BASE_URL = "https://clob.polymarket.com"


class AuthenticatedClobClient:
    """Wrapper around py_clob_client.ClobClient for authenticated operations.

    Lazily initialises on first use so the MCP server can start
    even without credentials (the public-read tools will still work).
    """

    def __init__(self) -> None:
        self._client: Any = None
        self._initialised = False
        # Safety limits (configurable via env)
        self.max_order_size = float(os.getenv("POLYMARKET_MAX_ORDER_SIZE", "100"))
        self.dry_run = os.getenv("POLYMARKET_DRY_RUN", "false").lower() == "true"

    def _ensure_client(self) -> Any:
        """Lazy-init: create py-clob-client on first authenticated call."""
        if self._initialised:
            return self._client

        private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
        if not private_key:
            raise RuntimeError(
                "POLYMARKET_PRIVATE_KEY not set in .env. "
                "Cannot use authenticated endpoints."
            )

        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import ApiCreds

        self._client = ClobClient(
            CLOB_BASE_URL,
            key=private_key,
            chain_id=POLYGON_CHAIN_ID,
        )

        # Use pre-configured API creds if available, otherwise derive them
        api_key = os.getenv("POLYMARKET_API_KEY")
        api_secret = os.getenv("POLYMARKET_API_SECRET")
        api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")

        if api_key and api_secret and api_passphrase:
            self._client.set_api_creds(ApiCreds(
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase,
            ))
            logger.info("Using pre-configured API credentials")
        else:
            creds = self._client.create_or_derive_api_creds()
            self._client.set_api_creds(creds)
            logger.info("Derived API credentials from private key")

        self._initialised = True
        return self._client

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def place_order(
        self,
        token_id: str,
        price: float,
        size: float,
        side: str,
        order_type: str = "GTC",
        tick_size: str = "0.01",
        neg_risk: bool = False,
    ) -> dict:
        """Create and submit a single order.

        Args:
            token_id: CLOB token ID for the outcome.
            price: Limit price (0.00-1.00).
            size: Number of shares.
            side: "BUY" or "SELL".
            order_type: GTC, FOK, GTD, or FAK.
            tick_size: Market tick size.
            neg_risk: Whether market uses negative risk.

        Returns:
            Order confirmation from the CLOB API.
        """
        # Safety guard
        order_value = price * size
        if order_value > self.max_order_size:
            raise ValueError(
                f"Order value ${order_value:.2f} exceeds max "
                f"${self.max_order_size:.2f}. "
                f"Set POLYMARKET_MAX_ORDER_SIZE to increase."
            )

        if self.dry_run:
            return {
                "dry_run": True,
                "would_place": {
                    "token_id": token_id,
                    "price": price,
                    "size": size,
                    "side": side,
                    "order_type": order_type,
                    "order_value": order_value,
                },
            }

        from py_clob_client.clob_types import OrderArgs, PartialCreateOrderOptions

        client = self._ensure_client()

        order_args = OrderArgs(
            token_id=token_id,
            price=price,
            size=size,
            side=side,
        )

        options = PartialCreateOrderOptions(
            tick_size=tick_size,
            neg_risk=neg_risk,
        )

        signed_order = client.create_order(order_args, options)
        logger.info(
            "Placing %s order: %s shares @ $%s for token %s...",
            side, size, price, token_id[:20],
        )
        result = client.post_order(signed_order, order_type)
        logger.info("Order placed: %s", result)
        return result

    def cancel_order(self, order_id: str) -> dict:
        """Cancel a specific open order by ID."""
        if self.dry_run:
            return {"dry_run": True, "would_cancel": order_id}

        client = self._ensure_client()
        logger.info("Cancelling order %s", order_id)
        result = client.cancel(order_id)
        return result

    def cancel_all_orders(self) -> dict:
        """Cancel ALL open orders (emergency kill switch)."""
        if self.dry_run:
            return {"dry_run": True, "would_cancel": "ALL"}

        client = self._ensure_client()
        logger.warning("CANCEL ALL ORDERS triggered")
        result = client.cancel_all()
        return result

    def cancel_orders(self, order_ids: list[str]) -> dict:
        """Cancel multiple orders by ID."""
        if self.dry_run:
            return {"dry_run": True, "would_cancel": order_ids}

        client = self._ensure_client()
        logger.info("Cancelling %d orders", len(order_ids))
        result = client.cancel_orders(order_ids)
        return result

    def get_order(self, order_id: str) -> dict:
        """Get details of a specific order."""
        client = self._ensure_client()
        return client.get_order(order_id)

    def get_open_orders(
        self,
        market: str | None = None,
        asset_id: str | None = None,
    ) -> dict:
        """Get all open/pending orders, optionally filtered."""
        from py_clob_client.clob_types import OpenOrderParams

        client = self._ensure_client()
        params = None
        if market or asset_id:
            kwargs: dict[str, str] = {}
            if market:
                kwargs["market"] = market
            if asset_id:
                kwargs["asset_id"] = asset_id
            params = OpenOrderParams(**kwargs)

        return client.get_orders(params)

    def get_balance_allowance(
        self,
        asset_type: str = "COLLATERAL",
        token_id: str = "",
    ) -> dict:
        """Get USDC balance and approval status.

        Args:
            asset_type: COLLATERAL (USDC) or CONDITIONAL (outcome tokens).
            token_id: Required for CONDITIONAL, ignored for COLLATERAL.
        """
        from py_clob_client.clob_types import AssetType, BalanceAllowanceParams

        client = self._ensure_client()
        at = AssetType.COLLATERAL if asset_type == "COLLATERAL" else AssetType.CONDITIONAL
        params = BalanceAllowanceParams(asset_type=at, token_id=token_id)
        return client.get_balance_allowance(params)
