import logging
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, ClosePositionRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from datetime import datetime, timedelta, timezone

TIMEFRAME_MAP = {
    "1Min": TimeFrame.Minute,
    "5Min": TimeFrame(5, "Min"),
    "15Min": TimeFrame(15, "Min"),
    "1Hour": TimeFrame.Hour,
    "1Day": TimeFrame.Day,
}

class Broker:
    def __init__(self, api_key, api_secret, paper=True):
        self.trading = TradingClient(api_key, api_secret, paper=paper)
        self.market = StockHistoricalDataClient(api_key, api_secret)

    def is_market_open(self):
        clock = self.trading.get_clock()
        return clock.is_open

    def account(self):
        return self.trading.get_account()

    def daily_pnl(self):
        # 종가 기준 실현손익 접근은 제한적이지만, 간단히 equity 변동으로 추정
        acct = self.account()
        return float(acct.equity) - float(acct.last_equity)

    def positions(self):
        return self.trading.get_all_positions()

    def get_position(self, symbol):
        try:
            return self.trading.get_open_position(symbol)
        except Exception:
            return None

    def submit_market_notional(self, symbol, side: str, notional_usd: float, extended_hours=False):
        req = MarketOrderRequest(
            symbol=symbol,
            notional=notional_usd,
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            extended_hours=extended_hours,
        )
        return self.trading.submit_order(req)

    def close_position(self, symbol):
        try:
            return self.trading.close_position(symbol, ClosePositionRequest())
        except Exception as e:
            logging.warning(f"close_position({symbol}) failed: {e}")
            return None

    def fetch_bars(self, symbol, timeframe_str: str, limit=300, tz="America/New_York"):
        tf = TIMEFRAME_MAP.get(timeframe_str, TimeFrame.Minute)
        # 끝 시간을 '지금'으로, 시작 시간은 적당히 과거로
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=7)  # 최근 7일 정도(분봉 기준)
        req = StockBarsRequest(symbol_or_symbols=symbol, timeframe=tf, start=start, end=end, limit=limit)
        bars = self.market.get_stock_bars(req)
        # 반환형: {symbol: [Bar,...]} → 리스트 반환
        return list(bars[symbol]) if symbol in bars else []