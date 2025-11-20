import duckdb
from pathlib import Path

# ---------------------------------------
# PATHS
# ---------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # btc_analytics/
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "btc_analytics.duckdb"

# ---------------------------------------
# BUILD MART
# ---------------------------------------
def build_fact_btc_daily():
    con = duckdb.connect(str(DB_PATH))

    con.execute("""
        CREATE OR REPLACE TABLE fact_btc_daily AS
        SELECT
            date,
            open,
            high,
            low,
            close,
            volume
        FROM raw_btc_daily
        ORDER BY date
    """)

    con.close()
    print("fact_btc_daily rebuilt in", DB_PATH)

# ---------------------------------------
# MAIN
# ---------------------------------------
def main():
    build_fact_btc_daily()

if __name__ == "__main__":
    main()
