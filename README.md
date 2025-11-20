Local BTC Analytics Pipeline

A fully local ELT pipeline that extracts historical BTC market data from Binance, loads and models it in DuckDB, and produces analytics-ready Parquet outputs for Power BI.
Runs entirely on your laptop with zero cloud dependencies.

Ingestion: Python (requests)
Storage & OLAP: DuckDB
Transformation: SQL models inside DuckDB
Orchestration: Prefect
BI Tool: Power BI
Environment: Python venv
Output: Single Parquet file refreshed by the pipeline

Architecture
Binance API
    ?
Python Extract
    ?
DuckDB Raw Layer (raw_btc_daily)
    ?
DuckDB Mart Layer (fact_btc_daily)
    ?
Parquet Export
    ?
Power BI Dashboard
    ?
Prefect Orchestration Controls All Steps

1. Quick Start
1.1 Setup

Create a virtual environment:

python -m venv .venv
.\.venv\Scripts\activate.ps1


Install dependencies:

pip install --upgrade pip
pip install requests pandas duckdb prefect


Project structure:

btc_analytics/
?
??? data/
??? src/
??? orchestrations/

1.2 Configuration

All data paths are automatically derived based on the project root using Path().
No manual configuration is required.

Optional adjustments:

Edit src/fetch_btc_raw.py to change symbol, interval, or limits.

Edit src/export_for_pbi.py if you want to export additional marts.

1.3 Run the Pipeline

Run the full ETL pipeline using Prefect:

python orchestrations\prefect_flow.py


This executes:

Extract BTC OHLCV from Binance

Load into DuckDB (raw_btc_daily)

Build mart table (fact_btc_daily)

Export Parquet (data/fact_btc_daily.parquet)

Power BI connects to the exported Parquet file.
Refreshing the report always loads the latest data.

1.4 Prefect UI (Optional)

Running the flow starts a temporary Prefect server at:

http://127.0.0.1:8090


Use it to inspect task logs and flow runs.

1.5 Access DuckDB UI
Using DuckDB CLI

Install DuckDB CLI:

winget install DuckDB.cli


Launch:

duckdb -ui


Attach the project database:

ATTACH 'data/btc_analytics.duckdb';


You can now browse:

raw_btc_daily

fact_btc_daily

1.6 Connect Power BI

Use the single exported Parquet file:

btc_analytics/data/fact_btc_daily.parquet


Steps:

Home ? Get Data ? Parquet

Select the file

Load

Click Refresh after the pipeline reruns

Because the pipeline overwrites the same file, no manual file updates are needed.

2. Manual Development Commands

Run components individually (without Prefect):

python src/fetch_btc_raw.py
python src/load_to_duckdb.py
python src/transform_to_marts.py
python src/export_for_pbi.py