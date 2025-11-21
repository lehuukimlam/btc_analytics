# Local BTC Analytics Pipeline

A fully local ELT pipeline that extracts historical BTC market data from Binance, loads and models it in DuckDB, and produces analytics-ready Parquet outputs for Power BI.
Runs entirely on your laptop with zero cloud dependencies.

**Ingestion:** Python (requests)  
**Storage & OLAP:** DuckDB  
**Transformation:** SQL models inside DuckDB  
**Orchestration:** Prefect  
**BI Tool:** Power BI  
**Environment:** Python venv  
**Output:** Single Parquet file refreshed by the pipeline

---

## Architecture


![Pipeline Architecture](assets/Flow.png)

The pipeline runs in four stages:

1. **Extract**  
   Pull OHLCV candles for BTC/USDT from the Binance API.

2. **Load**  
   Store raw data in a DuckDB database (`btc.duckdb`) under a `raw_btc_daily` table.

3. **Transform**  
   Build the analytics mart `fact_btc_daily` using SQL models (cleaning, resampling, adding return columns, etc.).

4. **Export**
   Export `fact_btc_daily` to `data/fact_btc_daily.parquet` for direct consumption in Power BI.

---

# 1. Quick Start

## 1.1 Setup

Create a virtual environment:

**Windows (PowerShell):**

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**macOS / Linux (bash/zsh):**

```python -m venv .venv
source .venv/bin/activate
```


Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Expected project structure:

```
btc_analytics/
│
├── data/
├── src/
└── orchestrations/
```

---

## 1.2 Configuration

All data paths are derived from the project root using pathlib.Path. No manual configuration is required.

Example (inside src/fetch_btc_raw.py):

```from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

DUCKDB_PATH = DATA_DIR / "btc.duckdb"
```

To change symbol or interval, edit src/fetch_btc_raw.py:

symbol (e.g. "BTCUSDT")

interval (e.g. "1d")

limit (number of candles to pull)

To change which marts get exported, edit src/export_for_pbi.pyDerive some findings

Once loaded in Power BI, you can build your own visuals or refer to the powerbi/ folder in this repository, which contains report screenshots and a short summary of the exploratory analysis performed on the dataset.

##  License

MIT — feel free to fork, build, or contribute.



