import pandas as pd

def bars_to_df(bars):
    """
    bars: list of Bar (alpaca-py)
    """
    if not bars:
        return pd.DataFrame(columns=["ts","o","h","l","c","v"])
    data = []
    for b in bars:
        data.append({
            "ts": pd.Timestamp(b.timestamp).tz_convert(None),
            "o": float(b.open),
            "h": float(b.high),
            "l": float(b.low),
            "c": float(b.close),
            "v": float(b.volume),
        })
    return pd.DataFrame(data).sort_values("ts").reset_index(drop=True)