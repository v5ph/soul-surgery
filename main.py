import asyncio
from src.engine import TradingEngine

if __name__ == "__main__":
    engine = TradingEngine()
    asyncio.run(engine.start())