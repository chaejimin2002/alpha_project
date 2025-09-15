import os
from dotenv import load_dotenv

load_dotenv()

CFG = {
    "exchange_id": os.getenv("EXCHANGE_ID", "binance"),
    "api_key": os.getenv("API_KEY", ""),
    "api_secret": os.getenv("API_SECRET", ""),
    "symbol": os.getenv("SYMBOL", "BTC/USDT"),
    "tf": os.getenv("TF", "1m"),
    "base_ccy": os.getenv("BASE_CCY", "USDT"),
    "order_size": float(os.getenv("ORDER_SIZE", "50")),
    "max_position": int(os.getenv("MAX_POSITION", "1")),
    "fee_bps": float(os.getenv("FEE_BPS", "10")),
    "slippage_bps": float(os.getenv("SLIPPAGE_BPS", "5")),
    "dry_run": os.getenv("DRY_RUN", "true").lower() == "true",
}