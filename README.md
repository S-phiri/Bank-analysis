# Bank customer analytics

SQL practice project: a small bank-customer table (10 sample customers across 5 Zambian branches) modelled in SQLite, with reusable views for churn and balance analysis and a Streamlit dashboard on top.

## What's here

- `schema.sql` — table definition; `data/bank_customers.csv` — sample data
- `views.sql` — 11 views: churn by branch, account type and income band; balances by branch, account type and tenure; high-value customers; branch performance; overall KPIs
- `export_views.py` — exports every view to `results/*.csv`
- `dashboard.py` — Streamlit + Plotly dashboard reading the views ([DASHBOARD_README.md](./DASHBOARD_README.md))

## Run

```bash
pip install -r requirements.txt
sqlite3 bank.db < schema.sql   # then load data and run views.sql
python export_views.py
streamlit run dashboard.py
```

The dataset is deliberately tiny, so the numbers are illustrative only.
