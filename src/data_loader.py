import ccxt
import pandas as pd
from .config import SYMBOL, TIMEFRAME, LIMIT

def fetch_data():
    """Fetches the last N candles from Binance (Public API)."""
    exchange = ccxt.binance()
    try:
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()