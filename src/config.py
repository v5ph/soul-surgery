import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
TIMEFRAME = "1h"  # Keep it simple for the demo
LIMIT = 100       # candles to fetch