# BTC Analytics – Power BI Dashboard (IDBI Framework)

## 1. Business Understanding
Crypto watchers compare periods, not single prices.  
The dashboard answers four core questions:

- How is BTC performing across multiple horizons (WoW, MoM, QoQ, YoY)?
- How far are we from the most recent Year-To-High (YTH)?
- What volatility regime are we in?
- Do two selected periods behave similarly?

Target users: traders and analysts who want fast, repeatable period comparison.

---

## 2. Information & Design

### Data Source & Schema
Data is imported directly from the Binance API through the ELT pipeline, stored in DuckDB, and exported to a single Parquet file for Power BI.

The model intentionally uses a minimal, transparent schema:

| Column   | Description                           |
|----------|----------------------------------------|
| `date`   | Daily timestamp (UTC)                 |
| `close`  | BTC closing price (USDT)              |
| `volume` | Daily traded BTC volume               |

Only these fields enter Power BI. All analytics derive from them.

### Dashboard Layout
- Price line chart with date slicers  
- KPI cards: WoW, MoM, QoQ, YoY  
- YTH drawdown card  
- 1-year rolling stdev card  
- Similarity score card using rule-based thresholds  
- Two-period slicer controls

---

## 3. Build & Modelling

### Data Preparation
Cleaning is automatic. The Binance API + DuckDB pipeline enforces types, date ordering, and duplicate handling.

### DAX Modelling
Power BI computes all analytics using:

- Daily Return (calculated column)  
- WoW, MoM, QoQ, YoY growth (DAX)  
- Drawdown from YTH (DAX)  
- 1-year Rolling Stdev of Daily Returns (DAX)  
- Rule-based Similarity Score (DAX)

---

### Similarity Rule (Matches the DAX Logic Exactly)

The similarity score checks four differences between Interval 1 and Interval 2:

- MoM Return difference ≤ **10%**  
- QoQ Return difference ≤ **30%**  
- Drawdown from Year Max difference ≤ **20%**  
- Next 90-Day Return difference ≤ **20%**

Each satisfied rule = **1 point**

Scoring:
- **4 points** → Intervals VERY similar  
- **2–3 points** → Intervals SOMEWHAT similar  
- **0–1 point** → Intervals NOT similar  

This rule is identical to the provided DAX.

---

## 4. Insight & Usage

Users can:
- Compare any two BTC periods with stable metrics  
- See volatility regime shifts  
- Measure how severe current drops are  
- Detect behavioural similarity using a transparent scoring rule  

**Refresh workflow:**  
Run the ELT pipeline → Parquet updates → Power BI Refresh.
