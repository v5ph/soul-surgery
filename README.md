# soul-surgery
RSI Alert System for Crypto & Stocks - 24/7 Discord Notifications

## 📁 Project Structure

```
soul-surgery/
├── .env                      # Your Discord Webhook URL (Do not commit)
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── config.yaml               # Bot configurations (symbols, strategies, params)
├── requirements.txt          # Python dependencies
├── main.py                   # Entry point - Standard polling mode
├── main_optimized.py         # Optimized polling with shared data cache
├── README.md                 # This file
└── src/
    ├── __init__.py
    ├── data_loader.py        # Universal data fetcher (Crypto + Stocks)
    ├── engine.py             # Main trading engine with 24/7 loop
    ├── optimized_engine.py   # Engine with shared cache for efficiency
    ├── notifier.py           # Discord alert sender (async)
    ├── indicators.py         # Technical indicator calculations
    └── strategies/
        ├── __init__.py
        ├── base.py           # Abstract base strategy class
        └── rsi_strategy.py   # RSI mean reversion strategy
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Discord Webhook
```bash
cp .env.example .env
# Edit .env and add your Discord webhook URL
```

### 3. Configure Bots
Edit `config.yaml` to add your trading pairs:

```yaml
bots:
  # Crypto (format: SYMBOL/USDT)
  - id: "btc_bot"
    pair: "BTC/USDT"
    timeframe: "1h"
    strategy: "rsi_mean_reversion"
    params:
      period: 14
      overbought: 70
      oversold: 30
      alert_cooldown: 3600
  
  # Stocks (format: TICKER)
  - id: "aapl_bot"
    pair: "AAPL"
    timeframe: "1h"
    strategy: "rsi_mean_reversion"
    params:
      period: 14
      overbought: 70
      oversold: 30
      alert_cooldown: 3600
```

### 4. Run
```bash
# Standard mode
python main.py

# Optimized mode (better for multiple bots on same symbols)
python main_optimized.py
```

## 📊 Supported Assets

| Type | Examples | Data Source |
|------|----------|-------------|
| **Crypto** | BTC/USDT, ETH/USDT, SOL/USDT | Binance (CCXT) |
| **Stocks** | AAPL, TSLA, MSFT, GOOGL | Yahoo Finance |
| **ETFs** | SPY, QQQ, VOO, IWM | Yahoo Finance |
| **Indices** | ^GSPC, ^DJI, ^IXIC | Yahoo Finance |

## ⚙️ Features

- ✅ **24/7 Operation** - Continuous monitoring with auto-recovery
- ✅ **Crypto + Stocks** - Unified system for all asset types
- ✅ **Alert Deduplication** - Configurable cooldown prevents spam
- ✅ **Parallel Execution** - All bots run simultaneously
- ✅ **Auto-retry Logic** - Handles network failures gracefully
- ✅ **Discord Alerts** - Real-time notifications with formatting
- ✅ **Extensible** - Easy to add new strategies

## 🔧 Configuration

### System Settings (`config.yaml`)
```yaml
system:
  update_interval: 60    # Seconds between cycles
  log_level: "INFO"      # Logging verbosity
```

### Bot Parameters
- `id`: Unique bot identifier
- `pair`: Trading pair (crypto) or ticker (stocks)
- `timeframe`: 1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.
- `strategy`: Strategy name (currently: "rsi_mean_reversion")
- `params`:
  - `period`: RSI calculation period (default: 14)
  - `overbought`: Upper threshold for SELL signals (default: 70)
  - `oversold`: Lower threshold for BUY signals (default: 30)
  - `alert_cooldown`: Seconds before repeating same signal (default: 3600)

## 🏃 Running 24/7

### Using nohup (Simple)
```bash
nohup python main.py > alerts.log 2>&1 &
tail -f alerts.log
```

### Using screen (Recommended)
```bash
screen -S soul-surgery
python main.py
# Detach: Ctrl+A, then D
# Reattach: screen -r soul-surgery
```

## 📦 Dependencies

- `ccxt` - Cryptocurrency exchange API
- `pandas` - Data manipulation
- `pandas_ta` - Technical analysis indicators
- `yfinance` - Stock market data
- `aiohttp` - Async HTTP for Discord webhooks
- `pyyaml` - YAML config parsing

## 🛠️ Architecture

### Data Flow
```
Config (YAML) → Engine → Data Loader → Strategy → Notifier
                   ↓
            Infinite Loop (60s)
                   ↓
         Crypto: Binance API (CCXT)
         Stocks: Yahoo Finance (yfinance)
                   ↓
         Technical Analysis (RSI)
                   ↓
         Signal Detection (Buy/Sell)
                   ↓
         Discord Alert (async)
```

### Key Components

- **Engine** - Orchestrates bot lifecycle, manages infinite loop
- **Data Loader** - Auto-detects asset type and fetches appropriate data
- **Strategy** - Analyzes price data and generates signals
- **Notifier** - Sends formatted alerts to Discord

## 🔒 Security

- Never commit `.env` file (contains webhook URL)
- `.gitignore` is pre-configured
- Use `.env.example` as template

## 📝 License

Private repository for business use