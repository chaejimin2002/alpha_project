import time, logging, signal
from datetime import datetime
import pandas as pd

from config import CFG
from broker import Broker
from datafeed import bars_to_df
from strategy import sma_signals
from risk import can_open_position, should_flatten_on_tp_sl, hit_daily_loss_guard

RUN = True

def handle_sigterm(*_):
    global RUN; RUN = False

signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

def last_entry_price_from_position(pos):
    try:
        # Alpaca position avg_entry_price
        return float(pos.avg_entry_price)
    except Exception:
        return None

def main():
    logging.basicConfig(level=getattr(logging, CFG["log_level"]), format="%(asctime)s %(levelname)s %(message)s")

    broker = Broker(CFG["api_key"], CFG["api_secret"], paper=CFG["paper"])
    symbol = CFG["symbol"]
    tf = CFG["timeframe"]

    last_signal_ts = None

    logging.info(f"Starting bot on {symbol} {tf} (paper={CFG['paper']})")
    while RUN:
        try:
            # 시장 시간 체크(프리/애프터 허용 옵션)
            if not CFG["extended_hours"]:
                if not broker.is_market_open():
                    logging.info("Market closed. Sleeping 60s.")
                    time.sleep(60)
                    continue

            # 데이터 수집 → 신호 계산
            bars = broker.fetch_bars(symbol, tf, limit=max(CFG["sma_slow"]*3, 200))
            df = bars_to_df(bars)
            if df.empty:
                time.sleep(CFG["poll_sec"])
                continue

            sigdf = sma_signals(df, CFG["sma_fast"], CFG["sma_slow"])
            row = sigdf.iloc[-1]
            sig = int(row["signal"])
            ts = pd.Timestamp(row["ts"]).to_pydatetime()

            # 같은 캔들 내 중복 매매 방지
            if last_signal_ts and ts == last_signal_ts:
                time.sleep(CFG["poll_sec"])
                continue

            # 일손실 가드
            daily_pnl = broker.daily_pnl()
            if hit_daily_loss_guard(daily_pnl, CFG["daily_max_loss"]):
                logging.warning(f"Daily loss guard triggered (PnL={daily_pnl:.2f}). Flatten & pause.")
                broker.close_position(symbol)
                time.sleep(60)
                continue

            # 현재 포지션 상태
            pos = broker.get_position(symbol)
            has_pos = pos is not None
            entry_px = last_entry_price_from_position(pos) if has_pos else None
            last_px = float(row["c"])

            # TP/SL
            if has_pos and should_flatten_on_tp_sl(entry_px, last_px, CFG["take_profit_pct"], CFG["stop_loss_pct"]):
                logging.info(f"[TP/SL EXIT] last={last_px:.2f} entry={entry_px:.2f}")
                broker.close_position(symbol)
                last_signal_ts = ts
                time.sleep(CFG["poll_sec"])
                continue

            # 시그널 매매
            if sig == 1:
                # 매수: 포지션 없고 한도 내면
                open_positions_count = 1 if has_pos else 0
                if can_open_position(open_positions_count, CFG["max_positions"]) and not has_pos:
                    logging.info(f"[BUY] {symbol} notional=${CFG['order_notional']}")
                    broker.submit_market_notional(symbol, "buy", CFG["order_notional"], CFG["extended_hours"])
                    last_signal_ts = ts
            elif sig == -1:
                # 매도: 포지션 있으면 전량 청산
                if has_pos:
                    logging.info(f"[SELL] {symbol} close position")
                    broker.close_position(symbol)
                    last_signal_ts = ts

        except Exception as e:
            logging.exception(e)

        time.sleep(CFG["poll_sec"])

if __name__ == "__main__":
    main()