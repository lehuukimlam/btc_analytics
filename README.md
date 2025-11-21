# Local BTC Analytics Pipeline

A fully local ELT pipeline that extracts historical BTC market data from Binance, loads and models it in DuckDB, and produces analytics‑ready Parquet outputs for Power BI. Runs entirely on your laptop with zero cloud dependencies.

**Ingestion:** Python (`requests`)  
**Storage & OLAP:** DuckDB  
**Transformation:** SQL models inside DuckDB  
**Orchestration:** Prefect  
**BI Tool:** Power BI  
**Environment:** Python `venv`  
**Output:** Single Parquet file refreshed by the pipeline

---

## Architecture

![Pipeline Architecture](assets/Flow.png)

---

# 1. Quick Start

## 1.1 Setup

Create and activate a virtual environment.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected project structure:
```
btc_analytics/
│
├── data/                    # Output Parquet + DuckDB database
├── src/                     # Pipeline modules
└── orchestrations/          # Prefect flow
```

---

## 1.2 Configuration

All paths are derived from the project root using `pathlib.Path`.  
No manual configuration is required.

Modify behaviour by editing:

- `src/fetch_btc_raw.py` — symbol, interval, limits  
- `src/export_for_pbi.py` — which marts get exported  

---

## 1.3 Run the Pipeline

Execute the full ELT flow:

```bash
python orchestrations/prefect_flow.py
```

This performs:

1. Extract BTC OHLCV from Binance  
2. Load into DuckDB (`raw_btc_daily`)  
3. Build the mart table (`fact_btc_daily`)  
4. Export a Parquet file (`data/fact_btc_daily.parquet`)  

The file is overwritten each run so Power BI always reads the latest output.

---

## 1.4 Connect Power BI

Use the Parquet file:

```
data/fact_btc_daily.parquet
```

Steps:

1. Home → Get Data → Parquet  
2. Select the file  
3. Load  
4. Refresh after rerunning the pipeline  

---

## 1.5 Derive findings

After loading into Power BI, build visualisations or check the optional `powerbi/` folder (if included) for screenshots and summary insights.

---

## License

MIT — feel free to fork, extend, or contribute.
