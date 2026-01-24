import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
import yfinance as yf
from datetime import datetime, timedelta

class AsyncDataLoader:
    def __init__(self):
        # Crypto exchange (Binance)
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        self._cache = {}  # Simple cache for recent data
        
        # Timeframe mapping for stocks (yfinance format)
        self.stock_intervals = {
            '1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
            '1h': '1h', '1d': '1d', '1wk': '1wk', '1mo': '1mo'
        }

    def _is_stock_symbol(self, symbol):
        """Detect if symbol is a stock (no slash) vs crypto (has slash)."""
        return '/' not in symbol
    
    async def _fetch_stock_data(self, symbol, timeframe, limit=100):
        """Fetch stock data using yfinance (runs in thread pool to avoid blocking)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._fetch_stock_sync, symbol, timeframe, limit)
    
    def _fetch_stock_sync(self, symbol, timeframe, limit):
        """Synchronous stock data fetch (called in thread pool)."""
        try:
            # Map timeframe to yfinance interval
            interval = self.stock_intervals.get(timeframe, '1h')
            
            # Calculate period based on limit and timeframe
            period_map = {
                '1m': f'{limit}m', '5m': f'{limit*5}m', '15m': f'{limit*15}m',
                '30m': f'{limit*30}m', '1h': f'{limit}h', '1d': f'{limit}d',
                '1wk': f'{limit}wk', '1mo': f'{limit}mo'
            }
            period = period_map.get(timeframe, '100d')
            
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return pd.DataFrame()
            
            # Normalize to match crypto format
            df = df.reset_index()
            df.columns = [col.lower() for col in df.columns]
            
            # Convert datetime to timestamp (milliseconds)
            if 'datetime' in df.columns:
                df['timestamp'] = pd.to_datetime(df['datetime']).astype(np.int64) // 10**6
                df = df.drop('datetime', axis=1)
            elif 'date' in df.columns:
                df['timestamp'] = pd.to_datetime(df['date']).astype(np.int64) // 10**6
                df = df.drop('date', axis=1)
            
            # Select and reorder columns to match crypto format
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df = df.tail(limit)  # Limit to requested number of candles
            
            return df.astype({'timestamp': np.int64, 'open': np.float64, 
                            'high': np.float64, 'low': np.float64, 
                            'close': np.float64, 'volume': np.float64})
        except Exception as e:
            print(f"Error fetching stock {symbol}: {e}")
            return pd.DataFrame()
    
    async def fetch_candles(self, symbol, timeframe, limit=100):
        """Universal fetch method - automatically detects crypto vs stocks."""
        max_retries = 3
        
        # Determine data source based on symbol format
        is_stock = self._is_stock_symbol(symbol)
        
        for attempt in range(max_retries):
            try:
                if is_stock:
                    # Fetch stock data via yfinance
                    df = await self._fetch_stock_data(symbol, timeframe, limit)
                else:
                    # Fetch crypto data via CCXT
                    bars = await self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
                    df = pd.DataFrame(
                        bars, 
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
                        dtype=np.float64
                    )
                    df['timestamp'] = df['timestamp'].astype(np.int64)
                
                return df
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"⚠️  Error fetching {symbol} (attempt {attempt+1}/{max_retries}): {e}")
                    print(f"   Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"❌ Failed to fetch {symbol} after {max_retries} attempts: {e}")
                    return pd.DataFrame()
    
    async def close(self):
        await self.exchange.close()