"""
Sales Data Analysis & Business Insights
=======================================
Streamlit dashboard backed only by data/sales_data.csv.
"""


from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from analysis.data_processor import (
    generate_business_insights,
    get_3d_bar_data,
    get_3d_scatter_data,
    get_3d_surface_data,
    get_category_performance,
    get_city_analysis,
    get_customer_segments,
    get_data_quality_summary,
    get_discount_profit_correlation,
    get_kpi_metrics,
    get_monthly_trends,
    get_payment_analysis,
    get_profit_margin_heatmap_data,
    get_regional_analysis,
    get_seasonal_analysis,
    get_shipping_analysis,
    get_strategic_recommendations,
    get_subcategory_performance,
    get_top_products,
    get_yoy_growth,
    load_and_clean_data,
)

st.set_page_config(
    page_title="Sales Analytics Dashboard | Anurag Verma",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    '<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">',
    unsafe_allow_html=True,
)

CUSTOM_CSS = """
<style>
:root { --panel: rgba(15, 23, 42, 0.86); --line: rgba(148, 163, 184, 0.18); --text: #F8FAFC; --text-soft: #CBD5E1; --muted: #94A3B8; --shadow: 0 18px 42px rgba(0, 0, 0, 0.28); }
.stApp { background: linear-gradient(180deg, #090D14 0%, #0B1120 48%, #111827 100%) !important; color: var(--text) !important; font-family: Inter, system-ui, sans-serif !important; }
.stApp > header, [data-testid="stHeader"] { background: transparent !important; }
.main .block-container { max-width: 1420px; padding-top: 1.2rem; padding-bottom: 2.5rem; }
h1, h2, h3, p, span, label { font-family: Inter, system-ui, sans-serif !important; letter-spacing: 0 !important; }
h1 { color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; background: none !important; font-size: clamp(2rem, 3vw, 3.2rem) !important; line-height: 1.05 !important; font-weight: 800 !important; }
[data-testid="stSidebar"] { background: #0B1120 !important; border-right: 1px solid var(--line) !important; }
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: var(--text-soft) !important; }
.brand-block { padding: 0.8rem 0.3rem 1.2rem; text-align: left; }
.brand-block .material-icons-round { color: #38BDF8; font-size: 2rem; }
.brand-block h1 { margin: 0.35rem 0 0.15rem !important; font-size: 1.25rem !important; }
.brand-block p { color: var(--muted); margin: 0; font-size: 0.78rem; }
.source-mini { border: 1px solid var(--line); background: rgba(56, 189, 248, 0.08); border-radius: 8px; color: var(--text-soft); line-height: 1.45; margin-top: 1rem; padding: 0.85rem; }
.source-mini .material-icons-round { color: #38BDF8; font-size: 1.1rem; vertical-align: middle; margin-right: 0.35rem; }
.page-hero { align-items: flex-end; border: 1px solid var(--line); background: linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(17, 24, 39, 0.88)); border-radius: 8px; box-shadow: var(--shadow); display: flex; justify-content: space-between; gap: 1.5rem; margin-bottom: 1rem; padding: 1.5rem 1.6rem; }
.page-hero h1 { margin: 0.35rem 0 0.45rem !important; }
.page-hero p { color: var(--text-soft); font-size: 0.98rem; line-height: 1.55; margin: 0; max-width: 820px; }
.eyebrow { align-items: center; color: #7DD3FC; display: inline-flex; font-size: 0.78rem; font-weight: 700; gap: 0.35rem; text-transform: uppercase; }
.eyebrow .material-icons-round { font-size: 1rem; }
.hero-source { display: grid; gap: 0.55rem; min-width: 190px; }
.hero-source span { background: rgba(2, 6, 23, 0.55); border: 1px solid var(--line); border-radius: 8px; color: var(--text); font-weight: 700; padding: 0.65rem 0.85rem; text-align: right; }
.metric-card, .recommendation-card, .insight-card { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; box-shadow: var(--shadow); }
.metric-card { min-height: 128px; overflow: hidden; padding: 1rem; position: relative; }
.metric-card::before, .recommendation-card::before { background: var(--accent); content: ''; height: 3px; left: 0; position: absolute; right: 0; top: 0; }
.metric-top { align-items: center; color: var(--muted); display: flex; font-size: 0.76rem; font-weight: 700; gap: 0.45rem; text-transform: uppercase; }
.metric-top .material-icons-round { color: var(--accent); font-size: 1.15rem; }
.metric-value { color: var(--text); font-size: clamp(1.25rem, 1.8vw, 1.75rem); font-weight: 800; margin-top: 0.8rem; overflow-wrap: anywhere; }
.metric-caption { color: var(--muted); font-size: 0.82rem; margin-top: 0.25rem; }
.section-header { align-items: center; display: flex; gap: 0.75rem; margin: 1.4rem 0 0.8rem; }
.section-header > .material-icons-round { align-items: center; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 8px; color: #38BDF8; display: inline-flex; height: 38px; justify-content: center; width: 38px; }
.section-header h2 { color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; background: none !important; font-size: 1.15rem !important; font-weight: 800 !important; margin: 0 !important; }
.section-header p { color: var(--muted); font-size: 0.82rem; margin: 0.1rem 0 0; }
.insight-card { align-items: flex-start; display: flex; gap: 0.9rem; margin-bottom: 0.8rem; min-height: 118px; padding: 1rem; }
.insight-card.success { border-left: 4px solid #22C55E; } .insight-card.info { border-left: 4px solid #38BDF8; } .insight-card.warning { border-left: 4px solid #F59E0B; } .insight-card.danger { border-left: 4px solid #EF4444; }
.insight-icon { align-items: center; border-radius: 8px; display: flex; flex: 0 0 40px; height: 40px; justify-content: center; }
.insight-icon.success { background: rgba(34, 197, 94, 0.15); color: #22C55E; } .insight-icon.info { background: rgba(56, 189, 248, 0.15); color: #38BDF8; } .insight-icon.warning { background: rgba(245, 158, 11, 0.15); color: #F59E0B; } .insight-icon.danger { background: rgba(239, 68, 68, 0.15); color: #EF4444; }
.insight-title, .recommendation-title { color: var(--text); font-size: 0.94rem; font-weight: 800; }
.insight-text, .recommendation-card p { color: var(--text-soft); font-size: 0.86rem; line-height: 1.55; margin: 0.35rem 0 0; }
.recommendation-card { margin-bottom: 0.8rem; min-height: 112px; overflow: hidden; padding: 1rem; position: relative; }
.recommendation-title { align-items: center; display: flex; gap: 0.5rem; }
.recommendation-title .material-icons-round { color: var(--accent); font-size: 1.2rem; }
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { background: rgba(15, 23, 42, 0.42); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.stButton > button, .stDownloadButton > button { background: #38BDF8 !important; border: 1px solid rgba(125, 211, 252, 0.45) !important; border-radius: 8px !important; color: #031018 !important; font-weight: 800 !important; }
.stButton > button:hover, .stDownloadButton > button:hover { background: #7DD3FC !important; border-color: #BAE6FD !important; }
[data-baseweb="select"] > div, [data-testid="stDateInput"] input, [data-testid="stSidebar"] .stRadio label { background: rgba(15, 23, 42, 0.78) !important; border-color: var(--line) !important; border-radius: 8px !important; color: var(--text) !important; }
[data-testid="stSidebar"] .stRadio label:hover { border-color: rgba(148, 163, 184, 0.28) !important; background: rgba(30, 41, 59, 0.78) !important; }
hr { border-color: var(--line) !important; margin: 1rem 0 !important; }
.footer { align-items: center; border-top: 1px solid var(--line); color: var(--muted); display: flex; font-size: 0.78rem; gap: 0.4rem; justify-content: center; margin-top: 2rem; padding: 1.2rem 0 0.2rem; }
.footer .material-icons-round { color: #38BDF8; font-size: 1rem; }
@media (max-width: 900px) { .page-hero { align-items: stretch; flex-direction: column; } .hero-source span { text-align: left; } .metric-card { min-height: 112px; } }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
COLORS = ["#38BDF8", "#22C55E", "#F59E0B", "#EF4444", "#A855F7", "#14B8A6", "#F97316", "#6366F1"]
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#D8DEE9", size=12),
    margin=dict(l=40, r=20, t=36, b=40),
    legend=dict(
        bgcolor="rgba(15,23,42,0.72)",
        bordercolor="rgba(148,163,184,0.18)",
        borderwidth=1,
        font=dict(size=11),
    ),
    hoverlabel=dict(bgcolor="#111827", bordercolor="#334155", font=dict(color="#F8FAFC")),
)


def format_currency(value):
    value = float(value) if pd.notna(value) else 0.0
    if abs(value) >= 1e7:
        return f"Rs {value / 1e7:.2f} Cr"
    if abs(value) >= 1e5:
        return f"Rs {value / 1e5:.2f} L"
    if abs(value) >= 1e3:
        return f"Rs {value / 1e3:.1f} K"
    return f"Rs {value:,.0f}"


def chart_layout(fig, height=390, show_x_grid=False, show_y_grid=True):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(showgrid=show_x_grid, gridcolor="rgba(148,163,184,0.14)")
    fig.update_yaxes(showgrid=show_y_grid, gridcolor="rgba(148,163,184,0.14)")
    return fig


def section_header(icon, title, caption=None):
    cap = f'<p>{caption}</p>' if caption else ""
    st.markdown(
        f"""
        <div class="section-header">
            <span class="material-icons-round">{icon}</span>
            <div><h2>{title}</h2>{cap}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(icon, title, value, caption, color="#38BDF8"):
    st.markdown(
        f"""
        <div class="metric-card" style="--accent:{color};">
            <div class="metric-top"><span class="material-icons-round">{icon}</span><span>{title}</span></div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_card(insight):
    st.markdown(
        f"""
        <div class="insight-card {insight['type']}">
            <div class="insight-icon {insight['type']}"><span class="material-icons-round">{insight['icon']}</span></div>
            <div><div class="insight-title">{insight['title']}</div><div class="insight-text">{insight['text']}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation(rec):
    st.markdown(
        f"""
        <div class="recommendation-card" style="--accent:{rec['color']};">
            <div class="recommendation-title"><span class="material-icons-round">{rec['icon']}</span><span>{rec['title']}</span></div>
            <p>{rec['text']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data(uploaded_bytes=None):
    if uploaded_bytes is None:
        return load_and_clean_data()
    return load_and_clean_data(BytesIO(uploaded_bytes))


uploaded_file = st.sidebar.file_uploader(
    "Use your verified sales CSV",
    type=["csv"],
    help="Upload a real sales export with the same schema as data/sales_data.csv.",
)
uploaded_bytes = uploaded_file.getvalue() if uploaded_file else None
data_source_label = uploaded_file.name if uploaded_file else "data/sales_data.csv"

try:
    df = load_data(uploaded_bytes)
except Exception as exc:
    if uploaded_file:
        st.error(f"Uploaded CSV could not be used: {exc}")
        st.info(
            "Minimum required fields are order id, order date, and revenue/sales amount. "
            "Common names like 'Order ID', 'Date', 'Sales', 'Amount', 'Product', 'Category', and 'Profit' are auto-detected. "
            "Showing the included data/sales_data.csv dashboard for now."
        )
        uploaded_file = None
        uploaded_bytes = None
        data_source_label = "data/sales_data.csv"
        df = load_data(None)
    else:
        st.error(f"Data could not be loaded: {exc}")
        st.stop()

quality = get_data_quality_summary(df)

with st.sidebar:
    st.markdown(
        """
        <div class="brand-block">
            <span class="material-icons-round">analytics</span>
            <h1>Sales Analytics</h1>
            <p>Verified CSV business dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Revenue & Trends",
            "Regional Analysis",
            "Product Performance",
            "Customer Insights",
            "Business Insights",
        ],
    )

    st.markdown("---")
    st.markdown("### Filters")

    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Year", years, default=years)

    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.date_input("Order date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    regions = sorted(df["Region"].unique())
    categories = sorted(df["Category"].unique())
    segments = sorted(df["Segment"].unique())

    selected_regions = st.multiselect("Region", regions, default=regions)
    selected_categories = st.multiselect("Category", categories, default=categories)
    selected_segments = st.multiselect("Segment", segments, default=segments)

    st.markdown(
        f"""
        <div class="source-mini">
            <span class="material-icons-round">dataset</span>
            <strong>{quality['rows']:,}</strong> source rows<br>
            <small>{data_source_label}</small><br>
            <small>{quality['start_date'].strftime('%d %b %Y')} to {quality['end_date'].strftime('%d %b %Y')}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

filtered_df = df[
    (df["Year"].isin(selected_years))
    & (df["Order_Date"] >= pd.to_datetime(start_date))
    & (df["Order_Date"] <= pd.to_datetime(end_date))
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Segment"].isin(selected_segments))
]

if filtered_df.empty:
    st.warning("No data matches the current filters. Please widen the filter selection.")
    st.stop()

kpis = get_kpi_metrics(filtered_df)
filtered_quality = get_data_quality_summary(filtered_df)

st.markdown(
    f"""
    <div class="page-hero">
        <div>
            <div class="eyebrow"><span class="material-icons-round">verified</span> Active source: {data_source_label}</div>
            <h1>Sales Data Analysis & Business Insights</h1>
            <p>Interactive dashboard for revenue, profit, products, customers, and regional performance. Upload a verified CSV or use the included CSV; no random rows are created at runtime.</p>
        </div>
        <div class="hero-source">
            <span>{filtered_quality['orders']:,} orders</span>
            <span>{filtered_quality['customers']:,} customers</span>
            <span>{filtered_quality['cities']:,} cities</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "Overview":
    cols = st.columns(4)
    with cols[0]:
        render_card("payments", "Total Revenue", format_currency(kpis["total_revenue"]), f"{kpis['total_orders']:,} orders", COLORS[0])
    with cols[1]:
        render_card("account_balance", "Total Profit", format_currency(kpis["total_profit"]), f"{kpis['profit_margin']:.1f}% margin", COLORS[1])
    with cols[2]:
        render_card("shopping_cart", "Avg Order Value", format_currency(kpis["avg_order_value"]), f"{int(kpis['total_quantity']):,} units sold", COLORS[2])
    with cols[3]:
        render_card("groups", "Unique Customers", f"{kpis['unique_customers']:,}", f"{kpis['avg_discount']:.1f}% avg discount", COLORS[4])

    col1, col2 = st.columns([1.65, 1])
    with col1:
        section_header("show_chart", "Revenue and Profit Trend", "Monthly movement from the filtered CSV records")
        monthly = get_monthly_trends(filtered_df)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Revenue"], mode="lines+markers", name="Revenue", line=dict(color=COLORS[0], width=3, shape="spline"), marker=dict(size=7), fill="tozeroy", fillcolor="rgba(56,189,248,0.10)", hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Profit"], mode="lines+markers", name="Profit", line=dict(color=COLORS[1], width=3, shape="spline"), marker=dict(size=6), hovertemplate="%{x}<br>Profit: Rs %{y:,.0f}<extra></extra>"))
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(chart_layout(fig, 410), use_container_width=True)

    with col2:
        section_header("donut_large", "Revenue Mix", "Category contribution")
        cat_perf = get_category_performance(filtered_df)
        fig = go.Figure(go.Pie(labels=cat_perf["Category"], values=cat_perf["Revenue"], hole=0.58, marker=dict(colors=COLORS), textinfo="label+percent", hovertemplate="%{label}<br>Revenue: Rs %{value:,.0f}<extra></extra>"))
        fig.update_layout(**PLOTLY_LAYOUT, height=410, showlegend=False, annotations=[dict(text=format_currency(kpis["total_revenue"]), x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#F8FAFC"))])
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        section_header("map", "Regional Revenue", "Where sales are strongest")
        regional = get_regional_analysis(filtered_df)
        fig = go.Figure(go.Bar(x=regional["Region"], y=regional["Revenue"], marker=dict(color=regional["Revenue"], colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[0]]]), text=[format_currency(v) for v in regional["Revenue"]], textposition="outside", hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"))
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

    with col4:
        section_header("inventory_2", "Top Products", "Ranked by revenue")
        top_products = get_top_products(filtered_df, n=10, metric="Revenue")
        fig = go.Figure(go.Bar(y=top_products["Product_Name"], x=top_products["Revenue"], orientation="h", marker=dict(color=top_products["Revenue"], colorscale=[[0, COLORS[5]], [1, COLORS[0]]]), text=[format_currency(v) for v in top_products["Revenue"]], textposition="outside", hovertemplate="%{y}<br>Revenue: Rs %{x:,.0f}<extra></extra>"))
        fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

elif page == "Revenue & Trends":
    monthly = get_monthly_trends(filtered_df)
    yoy = get_yoy_growth(filtered_df)
    quarterly = get_seasonal_analysis(filtered_df)

    cols = st.columns(4)
    if len(yoy) > 1:
        latest, previous = yoy.iloc[-1], yoy.iloc[-2]
        with cols[0]:
            render_card("trending_up", f"Revenue {int(latest['Year'])}", format_currency(latest["Revenue"]), f"{latest['Revenue_Growth']:.1f}% YoY", COLORS[0])
        with cols[1]:
            render_card("savings", f"Profit {int(latest['Year'])}", format_currency(latest["Profit"]), f"{latest['Profit_Growth']:.1f}% YoY", COLORS[1])
        with cols[2]:
            render_card("history", f"Revenue {int(previous['Year'])}", format_currency(previous["Revenue"]), f"{int(previous['Orders']):,} orders", COLORS[2])
        with cols[3]:
            render_card("person", "Customers", f"{int(latest['Customers']):,}", "latest selected year", COLORS[4])
    else:
        with cols[0]:
            render_card("trending_up", "Revenue", format_currency(kpis["total_revenue"]), "single-year selection", COLORS[0])
        with cols[1]:
            render_card("savings", "Profit", format_currency(kpis["total_profit"]), f"{kpis['profit_margin']:.1f}% margin", COLORS[1])

    section_header("stacked_line_chart", "Monthly Revenue and Cumulative Revenue", "Trend and running total")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"], y=monthly["Revenue"], name="Monthly Revenue", marker=dict(color=COLORS[0]), hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Cumulative_Revenue"], name="Cumulative Revenue", line=dict(color=COLORS[2], width=3), hovertemplate="%{x}<br>Cumulative: Rs %{y:,.0f}<extra></extra>"), secondary_y=True)
    fig.update_xaxes(tickangle=-35)
    fig.update_yaxes(title_text="Monthly", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative", secondary_y=True, showgrid=False)
    st.plotly_chart(chart_layout(fig, 430), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section_header("calendar_month", "Quarterly Performance")
        fig = go.Figure(go.Bar(x=quarterly["Quarter_Label"], y=quarterly["Revenue"], marker=dict(color=quarterly["Profit_Margin"], colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]]), text=[format_currency(v) for v in quarterly["Revenue"]], textposition="outside", hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"))
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    with col2:
        section_header("waterfall_chart", "Month-over-Month Growth")
        growth = monthly["Revenue_Growth"].fillna(0)
        fig = go.Figure(go.Bar(x=monthly["Month_Label"], y=growth, marker=dict(color=[COLORS[1] if v >= 0 else COLORS[3] for v in growth]), hovertemplate="%{x}<br>Growth: %{y:.1f}%<extra></extra>"))
        fig.update_xaxes(tickangle=-35)
        fig.update_yaxes(title="Growth %")
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

    section_header("view_in_ar", "3D Revenue Surface", "Month by category revenue")
    surface = get_3d_surface_data(filtered_df)
    fig = go.Figure(go.Surface(z=surface.values, x=list(range(len(surface.columns))), y=surface.index.tolist(), colorscale=[[0, "#0F172A"], [0.35, COLORS[0]], [0.7, COLORS[2]], [1, COLORS[3]]], opacity=0.94, hovertemplate="Category index: %{x}<br>Month: %{y}<br>Revenue: Rs %{z:,.0f}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT, height=520, scene=dict(xaxis=dict(title="Category", tickvals=list(range(len(surface.columns))), ticktext=surface.columns.tolist(), color="#CBD5E1"), yaxis=dict(title="Month", color="#CBD5E1"), zaxis=dict(title="Revenue", color="#CBD5E1"), bgcolor="rgba(0,0,0,0)", camera=dict(eye=dict(x=1.6, y=1.8, z=1.1))))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Regional Analysis":
    regional = get_regional_analysis(filtered_df)
    city_data = get_city_analysis(filtered_df, top_n=15)
    region_colors = {region: COLORS[i % len(COLORS)] for i, region in enumerate(regional["Region"])}

    reg_cols = st.columns(len(regional))
    for i, (_, row) in enumerate(regional.iterrows()):
        with reg_cols[i]:
            render_card("public", row["Region"], format_currency(row["Revenue"]), f"{row['Profit_Margin']:.1f}% margin | {int(row['Orders']):,} orders", region_colors[row["Region"]])

    section_header("grid_on", "Category Margin by Region", "Profit margin calculated as total profit divided by total revenue")
    heatmap = get_profit_margin_heatmap_data(filtered_df)
    fig = go.Figure(go.Heatmap(z=heatmap.values, x=heatmap.columns, y=heatmap.index, colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]], text=[[f"{v:.1f}%" for v in row] for row in heatmap.values], texttemplate="%{text}", hovertemplate="%{y} / %{x}<br>Margin: %{z:.1f}%<extra></extra>"))
    st.plotly_chart(chart_layout(fig, 390, show_x_grid=False, show_y_grid=False), use_container_width=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        section_header("apartment", "Top Cities", "Sorted by revenue")
        city_display = city_data.copy()
        city_display["Revenue"] = city_display["Revenue"].apply(format_currency)
        city_display["Profit"] = city_display["Profit"].apply(format_currency)
        city_display["Profit_Margin"] = city_display["Profit_Margin"].map(lambda x: f"{x:.1f}%")
        st.dataframe(city_display[["City", "State", "Region", "Revenue", "Profit", "Orders", "Profit_Margin"]], use_container_width=True, hide_index=True)
    with col2:
        section_header("radar", "Region Comparison")
        radar_cats = ["Revenue", "Profit", "Orders", "Quantity"]
        fig = go.Figure()
        for _, row in regional.iterrows():
            values = [row[c] / regional[c].max() if regional[c].max() else 0 for c in radar_cats]
            values.append(values[0])
            fig.add_trace(go.Scatterpolar(r=values, theta=radar_cats + [radar_cats[0]], name=row["Region"], fill="toself", line=dict(color=region_colors[row["Region"]])))
        fig.update_layout(**PLOTLY_LAYOUT, height=390, polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 1.1], showticklabels=False, gridcolor="rgba(148,163,184,0.16)")))
        st.plotly_chart(fig, use_container_width=True)

    section_header("view_in_ar", "3D City Category Revenue", "Top city/category combinations")
    bar_3d = get_3d_bar_data(filtered_df)
    fig = go.Figure()
    max_val = bar_3d.values.max() if bar_3d.size else 1
    for j, cat in enumerate(bar_3d.columns):
        for i, city in enumerate(bar_3d.index):
            value = bar_3d.loc[city, cat]
            if value > 0:
                fig.add_trace(go.Scatter3d(x=[i], y=[j], z=[value], mode="markers", marker=dict(size=max(5, min(20, value / max_val * 20)), color=COLORS[j % len(COLORS)], opacity=0.85), showlegend=False, hovertemplate=f"{city}<br>{cat}<br>Revenue: Rs {value:,.0f}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT, height=510, scene=dict(xaxis=dict(title="City", tickvals=list(range(len(bar_3d.index))), ticktext=bar_3d.index.tolist(), color="#CBD5E1"), yaxis=dict(title="Category", tickvals=list(range(len(bar_3d.columns))), ticktext=bar_3d.columns.tolist(), color="#CBD5E1"), zaxis=dict(title="Revenue", color="#CBD5E1"), bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Product Performance":
    col1, col2 = st.columns(2)
    with col1:
        section_header("trending_up", "Top 10 Products")
        top_10 = get_top_products(filtered_df, n=10, metric="Revenue")
        fig = go.Figure(go.Bar(y=top_10["Product_Name"], x=top_10["Revenue"], orientation="h", marker=dict(color=top_10["Profit_Margin"], colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]]), text=[format_currency(v) for v in top_10["Revenue"]], textposition="outside", hovertemplate="%{y}<br>Revenue: Rs %{x:,.0f}<extra></extra>"))
        fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
        st.plotly_chart(chart_layout(fig, 405), use_container_width=True)
    with col2:
        section_header("trending_down", "Bottom 10 Products")
        bottom_10 = get_top_products(filtered_df, n=10, metric="Revenue", ascending=True)
        fig = go.Figure(go.Bar(y=bottom_10["Product_Name"], x=bottom_10["Revenue"], orientation="h", marker=dict(color=bottom_10["Profit_Margin"], colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]]), text=[format_currency(v) for v in bottom_10["Revenue"]], textposition="outside", hovertemplate="%{y}<br>Revenue: Rs %{x:,.0f}<extra></extra>"))
        fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
        st.plotly_chart(chart_layout(fig, 405), use_container_width=True)

    section_header("account_tree", "Category and Sub-Category Treemap", "Size is revenue, color is profit margin")
    sub_perf = get_subcategory_performance(filtered_df)
    fig = px.treemap(sub_perf, path=["Category", "Sub_Category"], values="Revenue", color="Profit_Margin", color_continuous_scale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]], hover_data={"Revenue": ":,.0f", "Profit": ":,.0f", "Profit_Margin": ":.1f"})
    fig.update_layout(**PLOTLY_LAYOUT, height=440, coloraxis_colorbar=dict(title="Margin %"))
    fig.update_traces(hovertemplate="%{label}<br>Revenue: Rs %{value:,.0f}<br>Margin: %{color:.1f}%<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

    section_header("bubble_chart", "3D Product Analysis", "Quantity, average unit price, and profit")
    scatter_data = get_3d_scatter_data(filtered_df)
    fig = go.Figure()
    categories = scatter_data["Category"].unique().tolist()
    for idx, cat in enumerate(categories):
        cat_df = scatter_data[scatter_data["Category"] == cat]
        size_base = cat_df["Revenue"].max() or 1
        fig.add_trace(go.Scatter3d(x=cat_df["Quantity"], y=cat_df["Avg_Price"], z=cat_df["Profit"], mode="markers", name=cat, marker=dict(size=np.clip(cat_df["Revenue"] / size_base * 16, 5, 20), color=COLORS[idx % len(COLORS)], opacity=0.82, line=dict(width=1, color="rgba(255,255,255,0.25)")), text=cat_df["Product_Name"], hovertemplate="%{text}<br>Qty: %{x}<br>Avg Price: Rs %{y:,.0f}<br>Profit: Rs %{z:,.0f}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT, height=530, scene=dict(xaxis=dict(title="Quantity", color="#CBD5E1"), yaxis=dict(title="Avg Unit Price", color="#CBD5E1"), zaxis=dict(title="Profit", color="#CBD5E1"), bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Customer Insights":
    segments = get_customer_segments(filtered_df)
    payment = get_payment_analysis(filtered_df)
    seg_cols = st.columns(len(segments))
    for i, (_, row) in enumerate(segments.iterrows()):
        with seg_cols[i]:
            render_card("group", row["Segment"], format_currency(row["Revenue"]), f"{row['Revenue_Share']:.1f}% share | {row['Customers']} customers", COLORS[i % len(COLORS)])

    col1, col2 = st.columns(2)
    with col1:
        section_header("payments", "Payment Mode Distribution")
        fig = go.Figure(go.Pie(labels=payment["Payment_Mode"], values=payment["Revenue"], hole=0.55, marker=dict(colors=COLORS), textinfo="label+percent", hovertemplate="%{label}<br>Revenue: Rs %{value:,.0f}<extra></extra>"))
        fig.update_layout(**PLOTLY_LAYOUT, height=390)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        section_header("local_shipping", "Shipping Revenue")
        shipping = get_shipping_analysis(filtered_df)
        fig = go.Figure(go.Bar(x=shipping["Ship_Mode"], y=shipping["Revenue"], marker=dict(color=shipping["Revenue"], colorscale=[[0, COLORS[5]], [1, COLORS[0]]]), text=[format_currency(v) for v in shipping["Revenue"]], textposition="outside", hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"))
        st.plotly_chart(chart_layout(fig, 390), use_container_width=True)

    section_header("sell", "Discount Impact on Profitability", "Average profit by discount level and category")
    corr = get_discount_profit_correlation(filtered_df)
    fig = px.scatter(corr, x="Discount", y="Avg_Profit", color="Category", size="Count", size_max=28, color_discrete_sequence=COLORS, hover_data={"Avg_Revenue": ":,.0f", "Count": True})
    fig.update_layout(**PLOTLY_LAYOUT, height=420, xaxis=dict(title="Discount", tickformat=".0%"), yaxis=dict(title="Average Profit", tickformat=","))
    fig.update_traces(marker=dict(line=dict(width=1, color="rgba(255,255,255,0.22)")), hovertemplate="Discount: %{x:.0%}<br>Avg Profit: Rs %{y:,.0f}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

    section_header("view_in_ar", "3D Segment by Category", "Revenue, profit, and order volume")
    seg_data = filtered_df.groupby(["Segment", "Category"]).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Orders=("Order_ID", "nunique")).reset_index()
    fig = go.Figure()
    for i, seg in enumerate(seg_data["Segment"].unique()):
        seg_df = seg_data[seg_data["Segment"] == seg]
        size_base = seg_df["Revenue"].max() or 1
        fig.add_trace(go.Scatter3d(x=seg_df["Revenue"], y=seg_df["Profit"], z=seg_df["Orders"], mode="markers+text", name=seg, marker=dict(size=np.clip(seg_df["Revenue"] / size_base * 18, 6, 22), color=COLORS[i % len(COLORS)], opacity=0.84), text=seg_df["Category"], hovertemplate=f"{seg}<br>%{{text}}<br>Revenue: Rs %{{x:,.0f}}<br>Profit: Rs %{{y:,.0f}}<br>Orders: %{{z}}<extra></extra>"))
    fig.update_layout(**PLOTLY_LAYOUT, height=510, scene=dict(xaxis=dict(title="Revenue", color="#CBD5E1"), yaxis=dict(title="Profit", color="#CBD5E1"), zaxis=dict(title="Orders", color="#CBD5E1"), bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Business Insights":
    section_header("lightbulb", "Key Findings", "Generated from the current filter selection")
    insights = generate_business_insights(filtered_df, kpis)
    insight_cols = st.columns(2)
    for i, insight in enumerate(insights):
        with insight_cols[i % 2]:
            render_insight_card(insight)

    section_header("tips_and_updates", "Strategic Recommendations", "No hardcoded stories; these cards are calculated from the data")
    recs = get_strategic_recommendations(filtered_df)
    rec_cols = st.columns(2)
    for i, rec in enumerate(recs):
        with rec_cols[i % 2]:
            render_recommendation(rec)

    section_header("grid_on", "Profit Margin Heatmap", "Category by region")
    heatmap = get_profit_margin_heatmap_data(filtered_df)
    fig = go.Figure(go.Heatmap(z=heatmap.values, x=heatmap.columns, y=heatmap.index, colorscale=[[0, COLORS[3]], [0.5, COLORS[2]], [1, COLORS[1]]], text=[[f"{v:.1f}%" for v in row] for row in heatmap.values], texttemplate="%{text}", hovertemplate="%{y} / %{x}<br>Margin: %{z:.1f}%<extra></extra>"))
    st.plotly_chart(chart_layout(fig, 380, show_x_grid=False, show_y_grid=False), use_container_width=True)

    section_header("fact_check", "Data Source Check")
    qcols = st.columns(4)
    with qcols[0]:
        render_card("table_rows", "Filtered Rows", f"{filtered_quality['rows']:,}", f"from {data_source_label}", COLORS[0])
    with qcols[1]:
        render_card("event", "Date Range", f"{filtered_quality['start_date'].strftime('%b %Y')} - {filtered_quality['end_date'].strftime('%b %Y')}", "based on Order_Date", COLORS[1])
    with qcols[2]:
        render_card("category", "Products", f"{filtered_quality['products']:,}", "unique product names", COLORS[2])
    with qcols[3]:
        render_card("error", "Missing Values", f"{filtered_quality['missing_values']:,}", "after validation", COLORS[3])

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download filtered data", filtered_df.to_csv(index=False), "sales_data_filtered.csv", "text/csv", use_container_width=True)
    with col2:
        st.download_button("Download category summary", get_category_performance(filtered_df).to_csv(index=False), "category_summary.csv", "text/csv", use_container_width=True)

st.markdown(
    """
    <div class="footer">
        <span class="material-icons-round">analytics</span>
        Sales Data Analysis & Business Insights | Built by Anurag Verma | Streamlit, Plotly, Pandas
    </div>
    """,
    unsafe_allow_html=True,
)