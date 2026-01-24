# soul-surgery
Building RSI Alert bots for businesses

```
soul-surgery/
├── .env                  # Stores your Webhook URL (Do not commit this)
├── .gitignore            # Ignores .env and __pycache__
├── requirements.txt      # Dependencies
├── main.py               # Entry point (Run this)
└── src/
    ├── __init__.py
    ├── config.py         # Loads environment variables
    ├── data_loader.py    # Fetches live price data (CCXT)
    ├── indicators.py     # Calculates RSI (Pandas/Ta-Lib logic)
    └── notifier.py       # Handles Discord/Slack alerts
```