import requests
import pandas as pd
from pathlib import Path

# ---------------------------------------
# PATHS
# ---------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # btc_analytics/
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

RAW_PICKLE_PATH = DATA_DIR / "btc_raw.pkl"

# ---------------------------------------
# CONSTANTS
# ---------------------------------------
BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
LIMIT = 1000

# ---------------------------------------
# EXTRACT
# ---------------------------------------
def fetch_all_btc_klines():
    all_rows = []
    start_time = None

    while True:
        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT,
        }
        if start_time is not None:
            params["startTime"] = start_time

        resp = requests.get(BINANCE_URL, params=params, timeout=30)
        resp.raise_for_status()
        chunk = resp.json()
        if not chunk:
            break

        all_rows.extend(chunk)

        last_open_time = chunk[-1][0]
        next_start = last_open_time + 1

        if start_time is not None and next_start == start_time:
            break

        start_time = next_start

        if len(all_rows) >= 100000:
            break

    return all_rows

# ---------------------------------------
# TRANSFORM
# ---------------------------------------
def build_price_df(klines) -> pd.DataFrame:
    cols = [
        "open_time_ms",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time_ms",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore",
    ]

    df = pd.DataFrame(klines, columns=cols)

    num_cols = ["open", "high", "low", "close", "volume"]
    df[num_cols] = df[num_cols].astype(float)

    df["open_time"] = pd.to_datetime(df["open_time_ms"], unit="ms", utc=True)
    df["date"] = df["open_time"].dt.date

    return df.sort_values("open_time").reset_index(drop=True)

# ---------------------------------------
# MAIN
# ---------------------------------------
def main():
    print("Calling Binance...")
    klines = fetch_all_btc_klines()
    print("Raw rows:", len(klines))

    df = build_price_df(klines)
    print("Rows in df:", len(df))

    df.to_pickle(RAW_PICKLE_PATH)
    print("Saved", RAW_PICKLE_PATH)

if __name__ == "__main__":
    main()
