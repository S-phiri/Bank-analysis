# 🏦 Bank Customer Analytics Dashboard

Interactive web dashboard built with Streamlit for visualizing bank customer data.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `plotly` - Interactive charts

### 2. Make Sure Views Are Created

Before running the dashboard, ensure your database views are created:

```bash
# Using SQLite command line
sqlite3.exe bank.db < views.sql

# Or using Python
python -c "import sqlite3; exec(open('views.sql').read().replace('CREATE VIEW', 'CREATE VIEW IF NOT EXISTS'))"
```

### 3. Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your web browser at `http://localhost:8501`

## 📊 Dashboard Features

### Key Performance Indicators (KPIs)
- Total Customers
- Overall Churn Rate
- Average Balance
- Total Balance

### Analysis Tabs

1. **🔴 Churn Analysis**
   - Churn rate by branch (bar chart)
   - Churn rate by account type (pie chart)
   - Churn by income band

2. **💰 Balance Analysis**
   - Average balance by branch
   - Average balance by account type
   - Balance trends by customer tenure

3. **👥 Customer Segmentation**
   - Account type distribution
   - Branch distribution
   - High-value customers table

4. **🏢 Branch Performance**
   - Combined metrics visualization
   - Performance comparison table

5. **📋 Data Tables**
   - View all data tables
   - Download CSV exports

## 🎨 Features

- **Interactive Charts**: Built with Plotly for zoom, pan, and hover details
- **Real-time Data**: Connects directly to SQLite database
- **Responsive Design**: Works on desktop and mobile
- **Data Export**: Download any view as CSV
- **Caching**: Fast loading with Streamlit's caching

## 🔧 Troubleshooting

### Dashboard shows "No data found"
- Make sure you've run `views.sql` to create the views
- Verify `bank.db` exists in the same directory

### Charts not displaying
- Check that plotly is installed: `pip install plotly`
- Verify the views exist in the database

### Port already in use
- Streamlit will try to use port 8501
- If busy, it will automatically try the next available port

## 📝 Notes

- The dashboard uses `@st.cache_data` to cache database queries for better performance
- All data is loaded from SQL views (not raw tables)
- The dashboard automatically refreshes when you interact with filters

