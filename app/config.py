import os
from dotenv import load_dotenv

load_dotenv()

CFG = {
    "api_key": os.getenv("ALPACA_API_KEY_ID", ""),
    "api_secret": os.getenv("ALPACA_API_SECRET_KEY", ""),
    "paper": os.getenv("ALPACA_PAPER", "true").lower() == "true",
    "symbol": os.getenv("SYMBOL", "AAPL"),
    "timeframe": os.getenv("TIMEFRAME", "1Min"),
    "order_notional": float(os.getenv("ORDER_NOTIONAL_USD", "100")),
    "max_positions": int(os.getenv("MAX_OPEN_POSITIONS", "1")),
    "extended_hours": os.getenv("ALLOW_EXTENDED_HOURS", "false").lower() == "true",
    "sma_fast": int(os.getenv("SMA_FAST", "9")),
    "sma_slow": int(os.getenv("SMA_SLOW", "20")),
    "daily_max_loss": float(os.getenv("DAILY_MAX_LOSS_USD", "50")),
    "stop_loss_pct": float(os.getenv("STOP_LOSS_PCT", "0.02")),
    "take_profit_pct": float(os.getenv("TAKE_PROFIT_PCT", "0.04")),
    "poll_sec": int(os.getenv("POLL_SEC", "2")),
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "tz": os.getenv("TZ", "America/New_York"),
}