"""
Optimized polling engine - reduces API calls with shared data cache.
Good middle-ground between simple polling and WebSocket complexity.
"""

import asyncio
from src.optimized_engine import OptimizedTradingEngine

if __name__ == "__main__":
    engine = OptimizedTradingEngine()
    asyncio.run(engine.start())
