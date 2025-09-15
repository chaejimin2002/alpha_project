def backtest(signed_df, fee_bps=10):
    """
    signed_df: strategy.sma_signals(df) 결과
    룰: +1 시 시장가 매수(100% 현금→자산), -1 시 전량 매도(자산→현금)
    수수료만 고려하는 초간단 PnL
    """
    cash = 10000.0
    shares = 0.0
    last_px = None
    for _, r in signed_df.iterrows():
        px = r["c"]; last_px = px
        if r["signal"] == 1 and cash > 0:
            fee = cash * (fee_bps/1e4)
            invest = cash - fee
            shares = invest / px
            cash = 0.0
        elif r["signal"] == -1 and shares > 0:
            gross = shares * px
            fee = gross * (fee_bps/1e4)
            cash = gross - fee
            shares = 0.0
    # 마감 정산
    if shares > 0 and last_px:
        gross = shares * last_px
        fee = gross * (fee_bps/1e4)
        cash = gross - fee
        shares = 0.0
    return cash - 10000.0