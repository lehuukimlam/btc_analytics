import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "btc_analytics.duckdb"
PARQUET_PATH = DATA_DIR / "fact_btc_daily.parquet"

def export_fact():
    con = duckdb.connect(str(DB_PATH))

    con.execute(f"""
        COPY fact_btc_daily
        TO '{PARQUET_PATH}'
        (FORMAT PARQUET, OVERWRITE TRUE)
    """)

    con.close()
    print("Exported", PARQUET_PATH)

def main():
    export_fact()

if __name__ == "__main__":
    main()
