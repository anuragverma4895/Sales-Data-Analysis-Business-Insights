# Sales Data Analysis & Business Insights

A Streamlit + Plotly dashboard for sales analytics using either an uploaded verified CSV or the checked-in fallback source file at `data/sales_data.csv`.

The running app does not create random rows, mock orders, or sample values. Every KPI, chart, insight, recommendation, filter, and export is calculated from the active CSV loaded by `analysis/data_processor.py`.

## What It Shows

- Executive KPIs for revenue, profit, orders, average order value, customers, quantity, and discount.
- Revenue and profit trends by month, quarter, and year.
- Regional, city, category, sub-category, product, customer segment, payment, shipping, and discount analysis.
- 3D visualizations for revenue surfaces, city/category performance, product performance, and segment/category performance.
- Data-driven findings and strategic recommendations based on the current filters.
- CSV upload support for verified business exports, plus CSV export for filtered records and category summary.

## Data Source

Default fallback source: `data/sales_data.csv`

For actual business data, use the sidebar uploader in the app or replace `data/sales_data.csv` with your verified export.

Expected columns:

`Order_ID`, `Order_Date`, `Customer_ID`, `Customer_Name`, `Segment`, `City`, `State`, `Region`, `Category`, `Sub_Category`, `Product_Name`, `Quantity`, `Unit_Price`, `Discount`, `Revenue`, `Profit`, `Payment_Mode`, `Ship_Mode`

Current source coverage in the included CSV:

- 2,500 rows
- 2,500 unique orders
- 593 unique customers
- 134 unique products
- 22 cities
- Date range: 2023-01-01 to 2024-12-30

To use your own verified business data, upload a CSV from the sidebar or replace `data/sales_data.csv` with a file that follows the same schema. The app validates required columns and numeric/date fields on load.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Project Structure

```text
.
|-- app.py                    # Streamlit dashboard
|-- analysis/
|   |-- __init__.py
|   `-- data_processor.py     # Data validation and analytics functions
|-- data/
|   `-- sales_data.csv        # Dashboard source data
|-- assets/
|   `-- style.css             # Legacy stylesheet; app uses inline dashboard overrides
|-- requirements.txt
|-- render.yaml
|-- Procfile
|-- setup.sh
`-- README.md
```

## Deployment

Render and Streamlit Community Cloud can run this project with the standard command:

```bash
streamlit run app.py --server.port $PORT
```

No API keys or external services are required.