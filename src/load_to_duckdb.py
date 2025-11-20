import duckdb
import pandas as pd
from pathlib import Path

# ---------------------------------------
# PATHS
# ---------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # btc_analytics/
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

RAW_PICKLE_PATH = DATA_DIR / "btc_raw.pkl"
DB_PATH = DATA_DIR / "btc_analytics.duckdb"

# ---------------------------------------
# LOAD
# ---------------------------------------
def load_raw(df: pd.DataFrame):
    """
    Load full BTC daily dataframe into DuckDB table raw_btc_daily
    (truncate and reload each run).
    """
    con = duckdb.connect(str(DB_PATH))

    # register pandas df as a DuckDB relation
    con.register("btc_df", df)

    # Create table schema if it doesn't exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_btc_daily AS
        SELECT * FROM btc_df LIMIT 0
    """)

    # Truncate and reload
    con.execute("DELETE FROM raw_btc_daily")
    con.execute("INSERT INTO raw_btc_daily SELECT * FROM btc_df")

    con.close()

# ---------------------------------------
# MAIN
# ---------------------------------------
def main():
    if not RAW_PICKLE_PATH.exists():
        raise FileNotFoundError(f"Raw pickle not found at {RAW_PICKLE_PATH}")

    df = pd.read_pickle(RAW_PICKLE_PATH)
    load_raw(df)
    print("Loaded raw_btc_daily into", DB_PATH)

if __name__ == "__main__":
    main()
