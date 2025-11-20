import sys
from pathlib import Path

# ---------------------------------------
# Ensure project root is on sys.path
# ---------------------------------------
ROOT = Path(__file__).resolve().parents[1]  # .../btc_analytics
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prefect import flow, task
import pandas as pd

from src.fetch_btc_raw import fetch_all_btc_klines, build_price_df
from src.load_to_duckdb import load_raw
from src.transform_to_marts import build_fact_btc_daily
from src.export_for_pbi import export_fact


@task(name="extract_btc_from_binance")
def extract_task() -> pd.DataFrame:
    klines = fetch_all_btc_klines()
    df = build_price_df(klines)
    return df


@task(name="load_raw_into_duckdb")
def load_task(df: pd.DataFrame):
    load_raw(df)


@task(name="build_fact_table")
def transform_task():
    build_fact_btc_daily()


@task(name="export_parquet_for_pbi")
def export_task():
    export_fact()


@flow(name="btc_daily_pipeline")
def btc_daily_pipeline():
    df = extract_task()
    load_task(df)
    transform_task()
    export_task()


if __name__ == "__main__":
    btc_daily_pipeline()
