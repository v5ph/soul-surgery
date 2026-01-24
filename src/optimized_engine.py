import asyncio
import yaml
from collections import defaultdict
from .data_loader import AsyncDataLoader
from .notifier import send_alert, close_session
from .strategies.rsi_strategy import RsiMeanReversion

class OptimizedTradingEngine:
    """Polling-based engine with shared data cache (eliminates redundant API calls)."""
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.loader = AsyncDataLoader()
        self.active_bots = self.config['bots']
        
        # Strategy mapping
        self.strategy_map = {
            "rsi_mean_reversion": RsiMeanReversion
        }
        
        # Pre-instantiate strategies
        self.bot_strategies = {}
        for bot in self.active_bots:
            bot_id = bot['id']
            strategy_name = bot['strategy']
            StrategyClass = self.strategy_map.get(strategy_name)
            self.bot_strategies[bot_id] = StrategyClass(bot['params'])
        
        # Shared data cache: {(symbol, timeframe): DataFrame}
        self.data_cache = {}
    
    async def fetch_unique_data(self):
        """Fetch data for all unique symbol/timeframe combinations (avoids duplicates)."""
        unique_pairs = set()
        for bot in self.active_bots:
            unique_pairs.add((bot['pair'], bot['timeframe']))
        
        print(f"📊 Fetching {len(unique_pairs)} unique data streams...")
        
        # Fetch all unique combinations in parallel
        tasks = []
        for symbol, timeframe in unique_pairs:
            tasks.append(self._fetch_and_cache(symbol, timeframe))
        
        await asyncio.gather(*tasks)
    
    async def _fetch_and_cache(self, symbol: str, timeframe: str):
        """Fetch data and store in cache."""
        df = await self.loader.fetch_candles(symbol, timeframe)
        self.data_cache[(symbol, timeframe)] = df
    
    async def run_all_bots(self):
        """Run all bots using cached data (no redundant fetches)."""
        for bot in self.active_bots:
            symbol = bot['pair']
            timeframe = bot['timeframe']
            bot_id = bot['id']
            
            # Get data from cache
            df = self.data_cache.get((symbol, timeframe))
            
            if df is not None and not df.empty:
                strategy = self.bot_strategies[bot_id]
                signal, message = strategy.generate_signal(df)
                
                if signal:
                    print(f"[{symbol}] SIGNAL: {signal}")
                    await send_alert(symbol, message, signal)
                else:
                    print(f"[{symbol}] No Signal")
    
    async def start(self):
        print("=== SOUL SURGERY - OPTIMIZED POLLING ENGINE ===")
        print("📈 Shared cache reduces redundant API calls\n")
        
        try:
            while True:
                # 1. Fetch unique data (shared across bots)
                await self.fetch_unique_data()
                
                # 2. Run all bots using cached data
                await self.run_all_bots()
                
                print("Cycle complete. Sleeping...")
                await asyncio.sleep(self.config['system']['update_interval'])
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            await self.loader.close()
            await close_session()
