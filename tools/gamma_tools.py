"""MCP tool registrations for the Polymarket Gamma API."""

from __future__ import annotations

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from clients.gamma import GammaClient


def register_gamma_tools(mcp: FastMCP, gamma: GammaClient) -> None:
    """Register all Gamma read-only tools on the MCP server."""

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    @mcp.tool()
    async def search_events(
        query: Optional[str] = None,
        tag: Optional[str] = None,
        active: Optional[bool] = None,
        closed: Optional[bool] = None,
        order: Optional[str] = None,
        ascending: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """Search and discover Polymarket prediction events.

        Events function as high-level thematic containers grouping related markets (e.g., '2024 US Presidential Election' containing multiple candidate markets).
        This serves as the primary entry point for exploring the Polymarket ecosystem.

        Args:
            query (Optional[str]): A search term utilized to filter events by their title or descriptive slug.
            tag (Optional[str]): A thematic category tag for filtering (e.g., 'politics', 'crypto', 'sports').
            active (Optional[bool]): Set to true to strictly return currently active and open events.
            closed (Optional[bool]): Set to true to strictly return resolved or closed events.
            order (Optional[str]): The chronological or statistical field to sort results by (e.g., 'volume', 'created_at', 'end_date_iso').
            ascending (Optional[bool]): The sort direction. Defaults to false (descending order).
            limit (Optional[int]): The maximum number of paginated results to return.
            offset (Optional[int]): The pagination offset for results.
        """
        result = await gamma.get_events(
            slug=query,
            tag=tag,
            active=active,
            closed=closed,
            order=order,
            ascending=ascending,
            limit=limit,
            offset=offset,
        )
        return json.dumps(result)

    @mcp.tool()
    async def get_event(event_id: str) -> str:
        """Retrieve detailed, comprehensive information regarding a specific Polymarket event.

        Provides complete event metadata alongside a listing of all associated constituent markets, including their real-time prices, trading volumes, and specific outcome token identifiers.

        Args:
            event_id (str): The unique Gamma identifier for the event (formatted as a numeric string).
        """
        result = await gamma.get_event(event_id)
        return json.dumps(result)

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    @mcp.tool()
    async def search_markets(
        query: Optional[str] = None,
        tag: Optional[str] = None,
        active: Optional[bool] = None,
        closed: Optional[bool] = None,
        condition_id: Optional[str] = None,
        clob_token_ids: Optional[str] = None,
        order: Optional[str] = None,
        ascending: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """Search and discover specific, individual Polymarket prediction markets.

        Each individual market constitutes a singular yes/no predictive question utilizing tradeable outcome tokens.
        These markets provide the fundamental CLOB token IDs intrinsically required for pricing and order book evaluations.

        Args:
            query (Optional[str]): A search term utilized to filter markets by their title or descriptive slug.
            tag (Optional[str]): A thematic category tag for filtering.
            active (Optional[bool]): Set to true to strictly return currently active and successfully tradeable markets.
            closed (Optional[bool]): Set to true to strictly return definitively resolved or settled markets.
            condition_id (Optional[str]): Filter intrinsically by a unique on-chain condition ID.
            clob_token_ids (Optional[str]): Filter fundamentally by defined CLOB token IDs.
            order (Optional[str]): The specific field to sort the payload by.
            ascending (Optional[bool]): The structural sort direction.
            limit (Optional[int]): The maximum number of paginated results to return.
            offset (Optional[int]): The defined pagination offset limit.
        """
        result = await gamma.get_markets(
            slug=query,
            tag=tag,
            active=active,
            closed=closed,
            condition_id=condition_id,
            clob_token_ids=clob_token_ids,
            order=order,
            ascending=ascending,
            limit=limit,
            offset=offset,
        )
        return json.dumps(result)

    @mcp.tool()
    async def get_gamma_market(market_id_or_slug: str) -> str:
        """Retrieve detailed, comprehensive information regarding a single, specific Polymarket market natively via the Gamma API.

        Provides complete structural market metadata including the core question, qualitative description, array of outcomes, respective CLOB token IDs, global condition ID, cumulative volume, and definitive resolution parameters.

        Args:
            market_id_or_slug (str): The unique Gamma market mapping ID (numeric string) or URL-friendly slug.
        """
        result = await gamma.get_market(market_id_or_slug)
        return json.dumps(result)
