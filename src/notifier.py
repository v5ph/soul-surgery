import os
import asyncio
import aiohttp
from typing import Optional
from datetime import datetime

# Singleton session for connection reuse
_session: Optional[aiohttp.ClientSession] = None

async def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session

async def send_alert(symbol, rsi_value, signal_type):
    """Sends a formatted alert to Discord - optimized for alerts-only system."""
    webhook_url = os.getenv('WEBHOOK_URL')
    if not webhook_url:
        print("⚠️  Warning: WEBHOOK_URL not set - alerts disabled")
        return
    
    # Color coding for clarity
    color = 16711680 if signal_type == "SELL" else 65280  # Red or Green
    emoji = "📉" if signal_type == "SELL" else "📈"
    
    # Enhanced alert formatting
    data = {
        "embeds": [{
            "title": f"{emoji} {signal_type} Alert: {symbol}",
            "description": f"**RSI:** {rsi_value}\n**Action:** Monitor for {signal_type.lower()} opportunity",
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": "Soul Surgery Alert System"}
        }]
    }
    
    try:
        session = await get_session()
        async with session.post(webhook_url, json=data, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            if resp.status == 204:
                print(f"✅ Alert sent: {signal_type} for {symbol}")
            else:
                print(f"❌ Alert failed with status {resp.status}")
    except asyncio.TimeoutError:
        print(f"⏱️  Alert timeout for {symbol}")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

async def close_session():
    """Close the shared session on shutdown."""
    global _session
    if _session and not _session.closed:
        await _session.close()