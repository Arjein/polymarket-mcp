"""Async client for the Polymarket Data API.

Provides user positions, trade history, activity logs, and open interest.
Base URL: https://data-api.polymarket.com
"""

from __future__ import annotations

from typing import Any

import httpx

DATA_BASE_URL = "https://data-api.polymarket.com"


class DataClient:
    """Lightweight async wrapper around the Polymarket Data REST API."""

    def __init__(self, base_url: str = DATA_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers={"Accept": "application/json"},
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _get(self, path: str, params: dict | None = None) -> Any:
        client = await self._get_client()
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        resp = await client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Open interest (public, no auth)
    # ------------------------------------------------------------------

    async def get_open_interest(
        self,
        condition_id: str | None = None,
    ) -> Any:
        """Open interest for a market or global aggregate.

        Args:
            condition_id: Filter to a specific market. Omit for global OI.
        """
        params: dict[str, Any] = {}
        if condition_id:
            params["market"] = condition_id
        return await self._get("/oi", params=params or None)

    # ------------------------------------------------------------------
    # Positions (may need user address)
    # ------------------------------------------------------------------

    async def get_positions(
        self,
        user: str | None = None,
        market: str | None = None,
        event_id: str | None = None,
        size_threshold: float | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Current positions / holdings.

        Args:
            user: Wallet address to query positions for.
            market: Filter by condition ID.
            event_id: Filter by event ID.
            size_threshold: Min position size to include.
            limit: Max results.
            offset: Pagination offset.
        """
        params: dict[str, Any] = {
            "user": user,
            "market": market,
            "event": event_id,
            "sizeThreshold": size_threshold,
            "limit": limit,
            "offset": offset,
        }
        return await self._get("/positions", params=params)

    # ------------------------------------------------------------------
    # Trades history
    # ------------------------------------------------------------------

    async def get_trades(
        self,
        user: str | None = None,
        market: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Historical trade records.

        Args:
            user: Wallet address.
            market: Filter by condition ID.
            limit: Max results.
            offset: Pagination offset.
        """
        params: dict[str, Any] = {
            "user": user,
            "market": market,
            "limit": limit,
            "offset": offset,
        }
        return await self._get("/trades", params=params)

    # ------------------------------------------------------------------
    # Activity log
    # ------------------------------------------------------------------

    async def get_activity(
        self,
        user: str | None = None,
        market: str | None = None,
        activity_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Activity log (trades, splits, merges, rewards, redemptions).

        Args:
            user: Wallet address.
            market: Filter by condition ID.
            activity_type: One of TRADE, SPLIT, MERGE, REDEEM, REWARD, CONVERSION.
            limit: Max results.
            offset: Pagination offset.
        """
        params: dict[str, Any] = {
            "user": user,
            "market": market,
            "type": activity_type,
            "limit": limit,
            "offset": offset,
        }
        return await self._get("/activity", params=params)
