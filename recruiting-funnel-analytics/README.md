# Recruiting Funnel Analytics

An end-to-end pipeline to compute **stage conversion**, **time-to-fill**, and **source effectiveness** for the recruiting funnel, with exports for **Tableau/Power BI** dashboards.

## Problem
Recruiting teams need trustworthy metrics for **applied → hired** conversion, **stage drop-off**, and **time-to-fill** by role level, location, and source.

## Solution
- Normalize ATS events into canonical stages
- Compute **conversion rates**, **median time-to-fill**, and **D&I** tracking with a generic `diversity_flag`
- Export **dashboard-ready** aggregates and trend tables

## Tech Stack
- **Python** (pandas), **SQL** (example queries), **Tableau / Power BI**

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt
python scripts/build_funnel.py
python scripts/automation.py  # optional scheduled refresh mock
```

## Outputs (example)
- `data/derived/funnel_conversions.csv`
- `data/derived/time_to_fill.csv`
- `data/derived/source_effectiveness.csv`

## Notes
- Sample data are **synthetic** and safe to share.
