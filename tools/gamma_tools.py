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

        Events are top-level containers that group related markets. For example,
        an event "2024 US Presidential Election" may contain markets for each candidate.

        This is the best starting point for exploring what's available on Polymarket.

        Args:
            query: Search term to filter events by title or description (matched via slug).
            tag: Category tag to filter by (e.g. "politics", "crypto", "sports").
            active: If true, only return currently active/open events.
            closed: If true, only return resolved/closed events.
            order: Field to sort by (e.g. "volume", "created_at", "end_date_iso").
            ascending: Sort direction. False for descending (default).
            limit: Maximum number of results to return.
            offset: Pagination offset for results.
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
        """Get detailed information about a specific Polymarket event.

        Returns event metadata along with all markets belonging to this event,
        including their current prices, volumes, and outcome tokens.

        Args:
            event_id: The Gamma event ID (numeric string).
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
        """Search and discover individual Polymarket markets.

        Each market represents a single yes/no question with tradeable outcome tokens.
        Markets contain CLOB token IDs needed for price and order book queries.

        Args:
            query: Search term to filter markets by title (matched via slug).
            tag: Category tag to filter by.
            active: If true, only return currently active/tradeable markets.
            closed: If true, only return resolved/settled markets.
            condition_id: Filter by on-chain condition ID.
            clob_token_ids: Filter by CLOB token IDs.
            order: Field to sort by.
            ascending: Sort direction.
            limit: Maximum number of results.
            offset: Pagination offset.
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
        """Get detailed information about a specific Polymarket market.

        Returns full market metadata including question, description, outcomes,
        CLOB token IDs, condition ID, volume, and resolution details.

        Args:
            market_id_or_slug: The Gamma market ID (numeric) or URL slug.
        """
        result = await gamma.get_market(market_id_or_slug)
        return json.dumps(result)
