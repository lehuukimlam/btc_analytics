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


---

# 1. Quick Start

## 1.1 Setup

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate.ps1
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

All data paths are automatically derived based on the project root using `Path()`.
No manual configuration is required.

Optional adjustments:

- Edit `src/fetch_btc_raw.py` to change symbol, interval, or limits.
- Edit `src/export_for_pbi.py` if you want to export additional marts.

---

## 1.3 Run the Pipeline

Run the full ETL pipeline using Prefect:

```powershell
python orchestrations\prefect_flow.py
```

This executes:

1. Extract BTC OHLCV from Binance  
2. Load into DuckDB (`raw_btc_daily`)  
3. Build mart table (`fact_btc_daily`)  
4. Export Parquet (`data/fact_btc_daily.parquet`)

Power BI connects to the exported Parquet file.
Refreshing the report always loads the latest data.


---

## 1.4 Connect Power BI

Use the single exported Parquet file:

```text
btc_analytics/data/fact_btc_daily.parquet
```

Steps in Power BI Desktop:

1. Home → Get Data → Parquet  
2. Select `data/fact_btc_daily.parquet`  
3. Load  
4. Click **Refresh** whenever your pipeline reruns  

Because the pipeline overwrites the same file each run, no manual file changes are needed.

---

## 1.5 Devire some findings

Once loaded in Power BI, you can build your own visuals or refer to the powerbi/ folder in this repository, which contains report screenshots and a short summary of the exploratory analysis performed on the dataset.

```
