import time
import os
from src.data_loader import fetch_data
from src.indicators import calculate_rsi
from src.notifier import send_alert

# Load thresholds
OVERBOUGHT = int(os.getenv("RSI_OVERBOUGHT", 70))
OVERSOLD = int(os.getenv("RSI_OVERSOLD", 30))
SYMBOL = os.getenv("SYMBOL", "BTC/USDT")

def run_bot():
    print(f"--- STARTING SOUL SURGERY ENGINE [{SYMBOL}] ---")
    print("Waiting for signals...")
    
    while True:
        # 1. Get Data
        df = fetch_data()
        
        # 2. Analyze
        if not df.empty:
            rsi = calculate_rsi(df)
            price = df.iloc[-1]['close']
            
            print(f"Price: {price} | RSI: {rsi:.2f}")

            # 3. Trigger Logic
            if rsi > OVERBOUGHT:
                send_alert(SYMBOL, rsi, "SELL")
            elif rsi < OVERSOLD:
                send_alert(SYMBOL, rsi, "BUY")
        
        # 4. Wait (60 seconds)
        time.sleep(60)

if __name__ == "__main__":
    run_bot()