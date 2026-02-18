"""Async client for the Polymarket Gamma API.

Provides market/event discovery and rich metadata.
Base URL: https://gamma-api.polymarket.com
"""

from __future__ import annotations

from typing import Any

import httpx

GAMMA_BASE_URL = "https://gamma-api.polymarket.com"


class GammaClient:
    """Lightweight async wrapper around the Polymarket Gamma REST API."""

    def __init__(self, base_url: str = GAMMA_BASE_URL) -> None:
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
        # Strip None values so they aren't sent as query params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        resp = await client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    async def get_events(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order: str | None = None,
        ascending: bool | None = None,
        slug: str | None = None,
        tag: str | None = None,
        active: bool | None = None,
        closed: bool | None = None,
        id: str | None = None,
    ) -> list[dict]:
        """List / search events with optional filters.

        Args:
            limit: Max results to return.
            offset: Pagination offset.
            order: Field to order by (e.g. 'volume', 'created_at').
            ascending: Sort direction.
            slug: Filter by event slug.
            tag: Filter by category tag.
            active: If True, only active events.
            closed: If True, only closed events.
            id: Filter by event ID.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "ascending": ascending,
            "slug": slug,
            "tag": tag,
            "active": active,
            "closed": closed,
            "id": id,
        }
        return await self._get("/events", params=params)

    async def get_event(self, event_id: str) -> dict:
        """Detailed info for a single event, including its markets."""
        return await self._get(f"/events/{event_id}")

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    async def get_markets(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order: str | None = None,
        ascending: bool | None = None,
        slug: str | None = None,
        tag: str | None = None,
        active: bool | None = None,
        closed: bool | None = None,
        id: str | None = None,
        clob_token_ids: str | None = None,
        condition_id: str | None = None,
    ) -> list[dict]:
        """List / search markets with optional filters.

        Args:
            limit: Max results to return.
            offset: Pagination offset.
            order: Field to order by.
            ascending: Sort direction.
            slug: Filter by market slug.
            tag: Filter by category tag.
            active: If True, only active markets.
            closed: If True, only closed markets.
            id: Filter by Gamma market ID.
            clob_token_ids: Filter by CLOB token IDs.
            condition_id: Filter by on-chain condition ID.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "ascending": ascending,
            "slug": slug,
            "tag": tag,
            "active": active,
            "closed": closed,
            "id": id,
            "clob_token_ids": clob_token_ids,
            "condition_id": condition_id,
        }
        return await self._get("/markets", params=params)

    async def get_market(self, market_id_or_slug: str) -> dict | list:
        """Single market detail by Gamma ID or slug."""
        return await self._get(f"/markets/{market_id_or_slug}")
