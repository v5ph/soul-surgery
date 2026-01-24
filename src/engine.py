import asyncio
import yaml
from .data_loader import AsyncDataLoader
from .notifier import send_alert, close_session
from .strategies.rsi_strategy import RsiMeanReversion

class TradingEngine:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.loader = AsyncDataLoader()
        self.active_bots = self.config['bots']
        
        # Pre-initialize strategies to avoid recreating each cycle (significant speedup)
        self.strategy_map = {
            "rsi_mean_reversion": RsiMeanReversion
        }
        
        # Pre-instantiate strategies for each bot
        self.bot_strategies = {}
        for bot in self.active_bots:
            bot_id = bot['id']
            strategy_name = bot['strategy']
            StrategyClass = self.strategy_map.get(strategy_name)
            self.bot_strategies[bot_id] = StrategyClass(bot['params'])

    async def run_bot_cycle(self, bot_config):
        """Runs a single cycle for one specific bot configuration."""
        symbol = bot_config['pair']
        timeframe = bot_config['timeframe']
        bot_id = bot_config['id']
        
        try:
            # 1. Use pre-initialized strategy (avoid recreation overhead)
            strategy = self.bot_strategies[bot_id]
            
            # 2. Fetch Data
            df = await self.loader.fetch_candles(symbol, timeframe)
            
            if not df.empty:
                # 3. Get Signal
                signal, message = strategy.generate_signal(df)
                
                # 4. Act
                if signal:
                    print(f"[{symbol}] SIGNAL: {signal}")
                    # Now properly awaiting async function
                    await send_alert(symbol, message, signal)
                else:
                    print(f"[{symbol}] No Signal")
        except Exception as e:
            print(f"❌ Error in bot {bot_id}: {e} - Will retry next cycle")

    async def start(self):
        print("--- SOUL SURGERY V2: ENGINE STARTED ---")
        print(f"🤖 Running {len(self.active_bots)} bots")
        print(f"⏰ Update interval: {self.config['system']['update_interval']}s")
        print("📡 Data source: Binance REST API (24/7)\n")
        
        cycle_count = 0
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Cycle #{cycle_count} starting...")
                
                # Run all bots simultaneously (Parallel execution)
                tasks = [self.run_bot_cycle(bot) for bot in self.active_bots]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                print(f"✅ Cycle #{cycle_count} complete. Sleeping {self.config['system']['update_interval']}s...")
                await asyncio.sleep(self.config['system']['update_interval'])
        except KeyboardInterrupt:
            print("\n⏹️  Shutting down gracefully...")
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            print("🔄 Restarting in 30 seconds...")
            await asyncio.sleep(30)
            # Recursively restart
            await self.start()
        finally:
            await self.loader.close()
            await close_session()