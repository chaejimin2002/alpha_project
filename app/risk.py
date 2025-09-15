def can_open_position(current_open_positions, max_positions):
    return current_open_positions < max_positions

def should_flatten_on_tp_sl(entry_price, last_price, tp_pct, sl_pct):
    if entry_price is None or last_price is None:
        return False
    change = (last_price - entry_price) / entry_price
    if change >= tp_pct:
        return True
    if change <= -sl_pct:
        return True
    return False

def hit_daily_loss_guard(daily_pnl, daily_max_loss):
    return daily_pnl <= -abs(daily_max_loss)