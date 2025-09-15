import pandas as pd

def sma_signals(df: pd.DataFrame, fast=9, slow=20):
    out = df.copy()
    out["fast"] = out["c"].rolling(fast).mean()
    out["slow"] = out["c"].rolling(slow).mean()
    out["signal"] = 0
    cross_up = (out["fast"] > out["slow"]) & (out["fast"].shift(1) <= out["slow"].shift(1))
    cross_dn = (out["fast"] < out["slow"]) & (out["fast"].shift(1) >= out["slow"].shift(1))
    out.loc[cross_up, "signal"] = 1
    out.loc[cross_dn, "signal"] = -1
    return out.dropna().reset_index(drop=True)