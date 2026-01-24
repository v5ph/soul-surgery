import pandas_ta as ta

def calculate_rsi(df, period=14):
    """Applies RSI indicator to the dataframe."""
    if df.empty:
        return df
    
    # pandas_ta automatically appends a column named 'RSI_14'
    df.ta.rsi(length=period, append=True)
    
    # Rename for consistency if needed, or just return the last value
    current_rsi = df.iloc[-1][f'RSI_{period}']
    return current_rsi