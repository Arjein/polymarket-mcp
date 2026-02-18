# Polymarket MCP Server

An MCP (Model Context Protocol) server that gives LLM agents full access to [Polymarket](https://polymarket.com) — the world's largest prediction market. Discover markets, analyze trends, monitor positions, and execute trades.

<div align="center">

**34 tools** · **4 APIs** · **Read + Write** · **Safety Guards Built-in**

</div>

## Features

| Category | Tools | Auth Required |
|---|---|---|
| 🔍 **Market Discovery** | `search_events`, `search_markets`, `get_event`, `get_gamma_market` | ❌ |
| 📊 **Real-Time Pricing** | `get_price`, `get_midpoint`, `get_spread`, `get_order_book`, `get_last_trade_price` + batch variants | ❌ |
| 📈 **Analytics** | `get_price_history`, `get_open_interest` | ❌ |
| 🏦 **Account** | `get_positions`, `get_trade_history`, `get_activity` | Wallet address |
| 💰 **Trading** | `place_order`, `cancel_order`, `cancel_all_orders`, `get_open_orders`, `get_balance_allowance` | Private key |
| ⚙️ **Market Metadata** | `get_tick_size`, `get_neg_risk`, `get_fee_rate`, CLOB market listings | ❌ |

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
git clone https://github.com/Arjein/polymarket-mcp.git
cd polymarket-mcp
uv sync
```

### Configuration

```bash
cp .env.example .env
```

For **read-only** tools (market data, analytics): no configuration needed.

For **trading** tools: add your credentials to `.env`:

```env
POLYMARKET_PRIVATE_KEY=0xYourPrivateKey
POLYMARKET_WALLET_ADDRESS=0xYourWalletAddress
POLYMARKET_DRY_RUN=true        # Start with dry-run!
POLYMARKET_MAX_ORDER_SIZE=100  # Safety limit in USD
```

### Connect to Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "polymarket": {
      "command": "uv",
      "args": ["--directory", "/path/to/polymarket-mcp", "run", "server.py"]
    }
  }
}
```

### Run Standalone

```bash
uv run server.py
```

## Architecture

```
polymarket-mcp/
├── server.py              # MCP server entrypoint
├── clients/
│   ├── clob.py            # CLOB API (public reads + price history)
│   ├── gamma.py           # Gamma API (market/event discovery)
│   ├── data.py            # Data API (positions, trades, open interest)
│   └── auth_clob.py       # Authenticated CLOB (orders, balances)
├── tools/
│   ├── clob_tools.py      # 18 read-only CLOB tools
│   ├── gamma_tools.py     # 4 market discovery tools
│   ├── data_tools.py      # 5 analytics & account tools
│   └── trading_tools.py   # 7 authenticated trading tools
├── .env.example           # Configuration template
└── pyproject.toml         # Dependencies & metadata
```

### API Coverage

| API | Base URL | Purpose |
|---|---|---|
| **CLOB** | `clob.polymarket.com` | Order books, prices, spreads, market data |
| **Gamma** | `gamma-api.polymarket.com` | Market/event discovery, metadata, search |
| **Data** | `data-api.polymarket.com` | Positions, trades, activity, open interest |
| **CLOB Auth** | `clob.polymarket.com` | Order placement/cancellation, balances |

## Safety Guards

The trading tools include built-in safety mechanisms:

- **Dry-run mode** (`POLYMARKET_DRY_RUN=true`): Orders are simulated and returned as JSON without executing. Enabled by default.
- **Max order size** (`POLYMARKET_MAX_ORDER_SIZE`): Orders exceeding this USD value are rejected. Default: $100.
- **Lazy authentication**: The server starts without credentials — read-only tools work immediately. Auth is only initialized when a trading tool is first called.

## Tool Reference

<details>
<summary><strong>Market Discovery (4 tools)</strong></summary>

| Tool | Description |
|---|---|
| `search_events` | Search events by query, tag, active/closed status |
| `get_event` | Get event details including all child markets |
| `search_markets` | Search markets with filters (volume, tag, status) |
| `get_gamma_market` | Get full market metadata by ID or slug |

</details>

<details>
<summary><strong>Real-Time Pricing (10 tools)</strong></summary>

| Tool | Description |
|---|---|
| `get_price` | Best bid/ask price for a token |
| `get_midpoint` / `get_midpoints` | Mid-market price (single / batch) |
| `get_spread` / `get_spreads` | Bid-ask spread (single / batch) |
| `get_order_book` / `get_order_books` | Full order book depth (single / batch) |
| `get_last_trade_price` / `get_last_trades_prices` | Last executed price (single / batch) |

</details>

<details>
<summary><strong>Analytics (2 tools)</strong></summary>

| Tool | Description |
|---|---|
| `get_price_history` | Historical time-series with configurable interval and fidelity |
| `get_open_interest` | Total shares outstanding for a market |

</details>

<details>
<summary><strong>Account Management (3 tools)</strong></summary>

| Tool | Description |
|---|---|
| `get_positions` | Current holdings with P&L breakdown |
| `get_trade_history` | Historical executed trades |
| `get_activity` | Full audit trail (trades, splits, merges, rewards) |

</details>

<details>
<summary><strong>Trading (7 tools)</strong></summary>

| Tool | Description |
|---|---|
| `place_order` | Place a limit order (BUY/SELL, GTC/FOK/GTD/FAK) |
| `cancel_order` | Cancel a specific order |
| `cancel_orders` | Cancel multiple orders |
| `cancel_all_orders` | Emergency kill switch — cancel everything |
| `get_open_orders` | List all pending orders |
| `get_order` | Get order status and details |
| `get_balance_allowance` | Check USDC balance and approvals |

</details>

<details>
<summary><strong>CLOB Metadata (6 tools)</strong></summary>

| Tool | Description |
|---|---|
| `clob_health_check` | API health check |
| `clob_server_time` | Server timestamp |
| `get_clob_markets` / `get_clob_simplified_markets` | Browse CLOB market listings |
| `get_tick_size` / `get_neg_risk` / `get_fee_rate` | Market trading parameters |
| `get_market_trades_events` | Live trade feed for a market |

</details>

## Example Usage

Once connected to Claude Desktop, you can ask:

> "What are the hottest markets on Polymarket right now?"

> "Show me the Bitcoin price history over the last week"

> "What's the order book depth for the Fed rate decision market?"

> "Place a dry-run buy order for 100 YES shares at $0.35 on the Super Bowl market"

## ⚠️ Disclaimer

This software is provided for **educational and informational purposes only**. It is not financial advice.

- **Trading prediction markets involves risk.** You may lose some or all of your funds.
- The authors are **not responsible** for any financial losses incurred through the use of this software.
- **You are solely responsible** for your own trading decisions and for complying with all applicable laws and regulations in your jurisdiction.

By using this software, you acknowledge and accept these risks.

## License

MIT
