import requests
import json
from .config import WEBHOOK_URL

def send_alert(symbol, rsi_value, signal_type):
    """Sends a formatted embed to Discord."""
    color = 16711680 if signal_type == "SELL" else 65280 # Red or Green
    
    data = {
        "embeds": [{
            "title": f"🚨 {signal_type} SIGNAL: {symbol}",
            "description": f"RSI hit **{rsi_value:.2f}** on the 1H timeframe.",
            "color": color,
            "footer": {"text": "Soul Surgery | Algo Engine"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=data)
        print(f"Alert sent: {signal_type} for {symbol}")
    except Exception as e:
        print(f"Failed to send alert: {e}")