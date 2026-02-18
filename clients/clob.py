"""Async client for the Polymarket CLOB (Central Limit Order Book) API.

Covers all public (Level-0, no-auth) endpoints.
Base URL: https://clob.polymarket.com
"""

from __future__ import annotations

import httpx

CLOB_BASE_URL = "https://clob.polymarket.com"


class ClobClient:
    """Lightweight async wrapper around the Polymarket CLOB REST API."""

    def __init__(self, base_url: str = CLOB_BASE_URL) -> None:
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

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _get(self, path: str, params: dict | None = None) -> dict | list | str:
        client = await self._get_client()
        resp = await client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def _post(self, path: str, json_body: list | dict | None = None) -> dict | list:
        client = await self._get_client()
        resp = await client.post(path, json=json_body)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Health / meta
    # ------------------------------------------------------------------

    async def get_ok(self) -> str:
        """Health check – confirms the CLOB server is up."""
        return await self._get("/")

    async def get_server_time(self) -> dict:
        """Returns the current server timestamp."""
        return await self._get("/time")

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    async def get_markets(self, next_cursor: str = "MA==") -> dict:
        """Paginated list of all CLOB markets."""
        return await self._get("/markets", params={"next_cursor": next_cursor})

    async def get_simplified_markets(self, next_cursor: str = "MA==") -> dict:
        """Paginated compact market list."""
        return await self._get("/simplified-markets", params={"next_cursor": next_cursor})

    async def get_sampling_markets(self, next_cursor: str = "MA==") -> dict:
        """Current sampling market set."""
        return await self._get("/sampling-markets", params={"next_cursor": next_cursor})

    async def get_sampling_simplified_markets(self, next_cursor: str = "MA==") -> dict:
        """Compact sampling market set."""
        return await self._get("/sampling-simplified-markets", params={"next_cursor": next_cursor})

    async def get_market(self, condition_id: str) -> dict:
        """Single market detail by condition ID."""
        return await self._get(f"/markets/{condition_id}")

    async def get_market_trades_events(self, condition_id: str) -> dict:
        """Live trade events for a market."""
        return await self._get(f"/live-activity/events/{condition_id}")

    # ------------------------------------------------------------------
    # Order book
    # ------------------------------------------------------------------

    async def get_order_book(self, token_id: str) -> dict:
        """Full order book (bids + asks) for a token."""
        return await self._get("/book", params={"token_id": token_id})

    async def get_order_books(self, token_ids: list[str]) -> list[dict]:
        """Batch order books for multiple tokens."""
        body = [{"token_id": tid} for tid in token_ids]
        return await self._post("/books", json_body=body)

    # ------------------------------------------------------------------
    # Prices
    # ------------------------------------------------------------------

    async def get_price(self, token_id: str, side: str) -> dict:
        """Best price for a token on a given side (BUY or SELL)."""
        return await self._get("/price", params={"token_id": token_id, "side": side})

    async def get_prices(self, params: list[dict]) -> list[dict]:
        """Batch prices. Each dict should have token_id and side."""
        return await self._post("/prices", json_body=params)

    async def get_midpoint(self, token_id: str) -> dict:
        """Mid-market price for a token."""
        return await self._get("/midpoint", params={"token_id": token_id})

    async def get_midpoints(self, token_ids: list[str]) -> list[dict]:
        """Batch midpoints."""
        body = [{"token_id": tid} for tid in token_ids]
        return await self._post("/midpoints", json_body=body)

    # ------------------------------------------------------------------
    # Spreads
    # ------------------------------------------------------------------

    async def get_spread(self, token_id: str) -> dict:
        """Bid-ask spread for a token."""
        return await self._get("/spread", params={"token_id": token_id})

    async def get_spreads(self, token_ids: list[str]) -> list[dict]:
        """Batch spreads."""
        body = [{"token_id": tid} for tid in token_ids]
        return await self._post("/spreads", json_body=body)

    # ------------------------------------------------------------------
    # Last trade prices
    # ------------------------------------------------------------------

    async def get_last_trade_price(self, token_id: str) -> dict:
        """Last executed trade price for a token."""
        return await self._get("/last-trade-price", params={"token_id": token_id})

    async def get_last_trades_prices(self, token_ids: list[str]) -> list[dict]:
        """Batch last trade prices."""
        body = [{"token_id": tid} for tid in token_ids]
        return await self._post("/last-trades-prices", json_body=body)

    # ------------------------------------------------------------------
    # Market metadata
    # ------------------------------------------------------------------

    async def get_tick_size(self, token_id: str) -> dict:
        """Minimum tick size for a token's market."""
        return await self._get("/tick-size", params={"token_id": token_id})

    async def get_neg_risk(self, token_id: str) -> dict:
        """Whether the token's market uses neg-risk."""
        return await self._get("/neg-risk", params={"token_id": token_id})

    async def get_fee_rate(self, token_id: str) -> dict:
        """Fee rate (in bps) for a token's market."""
        return await self._get("/fee-rate", params={"token_id": token_id})

    # ------------------------------------------------------------------
    # Price history
    # ------------------------------------------------------------------

    async def get_prices_history(
        self,
        token_id: str,
        *,
        interval: str | None = None,
        fidelity: int | None = None,
        start_ts: int | None = None,
        end_ts: int | None = None,
    ) -> dict:
        """Historical price time-series for a token.

        Args:
            token_id: CLOB token ID.
            interval: Preset window ending now – one of 1h, 6h, 1d, 1w, 1m, max.
                      Mutually exclusive with start_ts/end_ts.
            fidelity: Data resolution in minutes (e.g. 60 = hourly).
            start_ts: Start unix timestamp (UTC). Use with end_ts.
            end_ts:   End unix timestamp (UTC). Use with start_ts.
        """
        params: dict = {"market": token_id}
        if interval:
            params["interval"] = interval
        if fidelity is not None:
            params["fidelity"] = fidelity
        if start_ts is not None:
            params["startTs"] = start_ts
        if end_ts is not None:
            params["endTs"] = end_ts
        return await self._get("/prices-history", params=params)
