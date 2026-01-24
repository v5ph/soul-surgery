import pandas_ta as ta
from .base import BaseStrategy
import pandas as pd
import time

class RsiMeanReversion(BaseStrategy):
    def __init__(self, params):
        super().__init__(params)
        self._last_signal = None
        self._last_signal_time = 0
        # Alert cooldown: don't repeat same signal within this period (seconds)
        self._cooldown = params.get('alert_cooldown', 3600)  # Default: 1 hour
    
    def generate_signal(self, df):
        if df.empty:
            return None, None
        
        period = self.params.get('period', 14)
        rsi_col = f'RSI_{period}'
        
        # Only calculate RSI if not already present (avoid redundant calculations)
        if rsi_col not in df.columns:
            df.ta.rsi(length=period, append=True)
        
        # Use .iat for faster single-value access instead of .iloc
        current_rsi = df[rsi_col].iat[-1]
        
        overbought = self.params['overbought']
        oversold = self.params['oversold']
        
        # Determine signal
        signal = None
        if current_rsi > overbought:
            signal = "SELL"
        elif current_rsi < oversold:
            signal = "BUY"
        
        # Alert deduplication: prevent spamming same signal
        if signal:
            current_time = time.time()
            
            # Only send alert if:
            # 1. Signal changed (BUY -> SELL or vice versa)
            # 2. Or cooldown period expired
            if (self._last_signal != signal or 
                current_time - self._last_signal_time > self._cooldown):
                
                self._last_signal = signal
                self._last_signal_time = current_time
                return signal, f"RSI is {current_rsi:.2f}"
        
        return None, None