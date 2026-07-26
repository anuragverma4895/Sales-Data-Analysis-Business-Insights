"""
Sales Data Analysis & Business Insights
Streamlit dashboard using uploaded CSV/TSV/Excel or data/sales_data.csv.
"""

from io import BytesIO
import hashlib

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
    page_title="Sales Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root { --bg:#080d16; --panel:#0f172a; --panel2:#111c31; --line:rgba(148,163,184,.22); --text:#f8fafc; --soft:#cbd5e1; --muted:#94a3b8; }
.stApp { background:linear-gradient(180deg,#080d16,#0b1120 48%,#111827) !important; color:var(--text); }
.main .block-container { max-width:1420px; padding-top:1.1rem; padding-bottom:2rem; }
h1,h2,h3,p,span,label,div { font-family:Inter, system-ui, sans-serif !important; letter-spacing:0 !important; }
h1 { color:var(--text) !important; font-size:clamp(2rem,3vw,3.1rem) !important; font-weight:850 !important; line-height:1.05 !important; }
[data-testid="stSidebar"] { background:#0b1120 !important; border-right:1px solid var(--line); }
.hero,.card,.insight,.rec { background:rgba(15,23,42,.86); border:1px solid var(--line); border-radius:8px; box-shadow:0 18px 42px rgba(0,0,0,.25); }
.hero { display:flex; justify-content:space-between; gap:1.2rem; align-items:flex-end; padding:1.4rem 1.5rem; margin-bottom:1rem; }
.hero p { color:var(--soft); max-width:850px; line-height:1.55; }
.badge { display:inline-flex; align-items:center; border:1px solid rgba(56,189,248,.3); color:#7dd3fc; background:rgba(56,189,248,.1); border-radius:8px; padding:.25rem .55rem; font-size:.78rem; font-weight:800; text-transform:uppercase; }
.hero-stats { display:grid; gap:.55rem; min-width:190px; }
.hero-stats span { background:rgba(2,6,23,.58); border:1px solid var(--line); border-radius:8px; padding:.65rem .8rem; text-align:right; font-weight:800; }
.card { min-height:126px; padding:1rem; border-top:3px solid var(--accent); }
.card .label { color:var(--muted); font-size:.78rem; font-weight:800; text-transform:uppercase; }
.card .value { color:var(--text); font-size:clamp(1.25rem,1.8vw,1.8rem); font-weight:850; margin-top:.75rem; overflow-wrap:anywhere; }
.card .caption { color:var(--muted); font-size:.83rem; margin-top:.25rem; }
.section { display:flex; gap:.7rem; align-items:center; margin:1.35rem 0 .75rem; }
.section .mark { width:38px; height:38px; display:inline-flex; justify-content:center; align-items:center; border-radius:8px; background:rgba(56,189,248,.12); border:1px solid rgba(56,189,248,.25); color:#7dd3fc; font-weight:900; }
.section h2 { margin:0 !important; color:var(--text) !important; font-size:1.14rem !important; font-weight:850 !important; }
.section p { margin:.08rem 0 0; color:var(--muted); font-size:.82rem; }
.insight,.rec { min-height:108px; padding:1rem; margin-bottom:.8rem; }
.insight { display:flex; gap:.85rem; border-left:4px solid var(--accent); }
.insight .mini,.rec .mini { flex:0 0 38px; height:38px; border-radius:8px; background:rgba(56,189,248,.14); color:#7dd3fc; display:flex; align-items:center; justify-content:center; font-weight:900; }
.insight b,.rec b { color:var(--text); }
.insight p,.rec p { color:var(--soft); font-size:.86rem; line-height:1.55; margin:.25rem 0 0; }
.rec { border-top:3px solid var(--accent); }
[data-testid="stPlotlyChart"],[data-testid="stDataFrame"] { background:rgba(15,23,42,.42); border:1px solid var(--line); border-radius:8px; overflow:hidden; }
.stDownloadButton button,.stButton button { background:#38bdf8 !important; color:#031018 !important; border-radius:8px !important; font-weight:850 !important; border:1px solid #7dd3fc !important; }
.small-note { color:var(--muted); font-size:.8rem; line-height:1.45; }
@media (max-width:900px){ .hero{flex-direction:column; align-items:stretch;} .hero-stats span{text-align:left;} }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

COLORS = ["#38BDF8", "#22C55E", "#F59E0B", "#EF4444", "#A855F7", "#14B8A6", "#F97316", "#6366F1"]
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#D8DEE9", size=12),
    margin=dict(l=40, r=20, t=36, b=40),
    legend=dict(bgcolor="rgba(15,23,42,.72)", bordercolor="rgba(148,163,184,.18)", borderwidth=1),
    hoverlabel=dict(bgcolor="#111827", bordercolor="#334155", font=dict(color="#F8FAFC")),
)


def money(value):
    value = float(value) if pd.notna(value) else 0.0
    if abs(value) >= 1e7:
        return f"Rs {value / 1e7:.2f} Cr"
    if abs(value) >= 1e5:
        return f"Rs {value / 1e5:.2f} L"
    if abs(value) >= 1e3:
        return f"Rs {value / 1e3:.1f} K"
    return f"Rs {value:,.0f}"


def chart_layout(fig, height=390):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(gridcolor="rgba(148,163,184,.14)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.14)")
    return fig


def section(mark, title, caption=""):
    cap = f"<p>{caption}</p>" if caption else ""
    st.markdown(f'<div class="section"><span class="mark">{mark}</span><div><h2>{title}</h2>{cap}</div></div>', unsafe_allow_html=True)


def card(label, value, caption, color):
    st.markdown(
        f'<div class="card" style="--accent:{color}"><div class="label">{label}</div><div class="value">{value}</div><div class="caption">{caption}</div></div>',
        unsafe_allow_html=True,
    )


def insight_card(title, text, accent="#38BDF8", mark="IN"):
    st.markdown(
        f'<div class="insight" style="--accent:{accent}"><div class="mini">{mark}</div><div><b>{title}</b><p>{text}</p></div></div>',
        unsafe_allow_html=True,
    )


def rec_card(title, text, accent="#38BDF8", mark="RC"):
    st.markdown(
        f'<div class="rec" style="--accent:{accent}"><b>{mark} &nbsp; {title}</b><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


def answer_data_question(data, question):
    q = question.lower().strip()
    metrics = get_kpi_metrics(data)
    if not q:
        return ""
    if any(word in q for word in ["predict", "forecast", "next month", "future"]):
        monthly = get_monthly_trends(data)
        if len(monthly) < 2:
            return "Need at least two months of data to forecast the next month."
        x = np.arange(len(monthly))
        y = monthly["Revenue"].astype(float).to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        next_revenue = max(0, slope * len(monthly) + intercept)
        last_revenue = y[-1]
        change = ((next_revenue - last_revenue) / last_revenue * 100) if last_revenue else 0
        return f"Forecast: next month revenue is approximately {money(next_revenue)} ({change:+.1f}% vs latest month)."
    if "margin" in q:
        return f"Profit margin is {metrics['profit_margin']:.1f}% on the current filters."
    if "profit" in q:
        return f"Total profit is {money(metrics['total_profit'])}."
    if "revenue" in q or "sales" in q or "amount" in q:
        return f"Total revenue is {money(metrics['total_revenue'])} from {metrics['total_orders']:,} orders."
    if "order" in q:
        return f"There are {metrics['total_orders']:,} unique orders."
    if "customer" in q:
        return f"There are {metrics['unique_customers']:,} unique customers."
    lookups = {
        "category": ("Category", get_category_performance),
        "region": ("Region", get_regional_analysis),
        "city": ("City", get_city_analysis),
        "product": ("Product_Name", lambda df: get_top_products(df, n=10)),
        "segment": ("Segment", get_customer_segments),
        "payment": ("Payment_Mode", get_payment_analysis),
    }
    for word, (column, fn) in lookups.items():
        if word in q:
            ranked = fn(data)
            if ranked.empty:
                return f"No {word} data is available."
            row = ranked.sort_values("Revenue", ascending=False).iloc[0]
            return f"Top {word} is {row[column]} with {money(row['Revenue'])} revenue."
    top_cat = get_category_performance(data).iloc[0]
    return f"Summary: {money(metrics['total_revenue'])} revenue, {money(metrics['total_profit'])} profit, {metrics['total_orders']:,} orders. Top category is {top_cat['Category']}."


@st.cache_data(show_spinner=False)
def load_data(uploaded_name=None, uploaded_bytes=None):
    if uploaded_bytes is None:
        return load_and_clean_data()
    suffix = uploaded_name.lower().rsplit(".", 1)[-1] if uploaded_name and "." in uploaded_name else "csv"
    buffer = BytesIO(uploaded_bytes)
    if suffix in {"xlsx", "xls"}:
        raw_df = pd.read_excel(buffer)
    elif suffix == "tsv":
        raw_df = pd.read_csv(buffer, sep="\t")
    else:
        raw_df = pd.read_csv(buffer)
    return load_and_clean_data(raw_df)


uploaded_file = st.sidebar.file_uploader(
    "Upload sales data file",
    type=["csv", "tsv", "xlsx", "xls"],
    help="Common headers like Total Revenue, Total Profit, Item Type, Order ID, and Date are auto-detected.",
)
uploaded_bytes = uploaded_file.getvalue() if uploaded_file else None
source_label = uploaded_file.name if uploaded_file else "data/sales_data.csv"
source_key = hashlib.md5(uploaded_bytes or b"fallback-source").hexdigest()[:10]

try:
    df = load_data(source_label, uploaded_bytes)
except Exception as exc:
    if uploaded_file:
        st.error(f"Uploaded file could not be used: {exc}")
        st.info("Minimum required fields are order id, order date, and revenue/sales amount. Showing fallback data/sales_data.csv for now.")
        source_label = "data/sales_data.csv"
        df = load_data(None, None)
    else:
        st.error(f"Data could not be loaded: {exc}")
        st.stop()

quality = get_data_quality_summary(df)
source_kpis = get_kpi_metrics(df)

with st.sidebar:
    st.markdown("<h1 style='font-size:1.5rem'>Sales Analytics</h1><p class='small-note'>Live dashboard from your uploaded file or fallback CSV.</p>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["Overview", "Revenue & Trends", "Regional Analysis", "Product Performance", "Customer Insights", "Business Insights"], key=f"page_{source_key}")
    st.markdown("---")
    st.markdown("### Filters")
    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Year", years, default=years, key=f"years_{source_key}")
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.date_input("Order date", value=(min_date, max_date), min_value=min_date, max_value=max_date, key=f"dates_{source_key}")
    start_date, end_date = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)
    selected_regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()), key=f"regions_{source_key}")
    selected_categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()), key=f"categories_{source_key}")
    selected_segments = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()), key=f"segments_{source_key}")
    st.markdown(f"<div class='small-note'><b>{quality['rows']:,}</b> rows<br>{source_label}<br>{quality['start_date'].strftime('%d %b %Y')} to {quality['end_date'].strftime('%d %b %Y')}</div>", unsafe_allow_html=True)

if uploaded_file:
    st.success(
        f"Loaded {source_label}: {quality['rows']:,} rows, {quality['orders']:,} orders, "
        f"{money(source_kpis['total_revenue'])} revenue. Filters and charts now use this uploaded file."
    )
    with st.expander("Uploaded data preview and detected columns", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            card("Rows", f"{quality['rows']:,}", "uploaded data", COLORS[0])
        with c2:
            card("Date Range", f"{quality['start_date'].strftime('%b %Y')} - {quality['end_date'].strftime('%b %Y')}", "detected dates", COLORS[1])
        with c3:
            card("Revenue", money(source_kpis["total_revenue"]), "detected sales", COLORS[2])
        with c4:
            card("Products/Categories", f"{quality['products']:,}", "detected labels", COLORS[4])
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)
filtered_df = df[
    (df["Year"].isin(selected_years))
    & (df["Order_Date"] >= pd.to_datetime(start_date))
    & (df["Order_Date"] <= pd.to_datetime(end_date))
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Segment"].isin(selected_segments))
]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please widen the selection.")
    st.stop()

kpis = get_kpi_metrics(filtered_df)
filtered_quality = get_data_quality_summary(filtered_df)

st.markdown(
    f"""
    <div class="hero">
      <div>
        <span class="badge">Active source: {source_label}</span>
        <h1>Sales Data Analysis & Business Insights</h1>
        <p>Upload CSV, TSV, or Excel and get live dashboard answers from that file. The app auto-maps common sales headers and never creates random rows at runtime.</p>
      </div>
      <div class="hero-stats"><span>{filtered_quality['orders']:,} orders</span><span>{filtered_quality['customers']:,} customers</span><span>{filtered_quality['cities']:,} cities</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

question = st.text_input("Ask your data", placeholder="Example: total revenue, top region, top product, profit margin, predict next month revenue", key=f"question_{source_key}")
if question:
    st.success(answer_data_question(filtered_df, question))

if page == "Overview":
    cols = st.columns(4)
    with cols[0]: card("Total Revenue", money(kpis["total_revenue"]), f"{kpis['total_orders']:,} orders", COLORS[0])
    with cols[1]: card("Total Profit", money(kpis["total_profit"]), f"{kpis['profit_margin']:.1f}% margin", COLORS[1])
    with cols[2]: card("Avg Order Value", money(kpis["avg_order_value"]), f"{int(kpis['total_quantity']):,} units", COLORS[2])
    with cols[3]: card("Unique Customers", f"{kpis['unique_customers']:,}", f"{kpis['avg_discount']:.1f}% avg discount", COLORS[4])

    col1, col2 = st.columns([1.6, 1])
    with col1:
        section("TR", "Revenue and Profit Trend", "Monthly movement from current filters")
        monthly = get_monthly_trends(filtered_df)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Revenue"], mode="lines+markers", name="Revenue", line=dict(color=COLORS[0], width=3), fill="tozeroy", hovertemplate="%{x}<br>Revenue: Rs %{y:,.0f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Profit"], mode="lines+markers", name="Profit", line=dict(color=COLORS[1], width=3), hovertemplate="%{x}<br>Profit: Rs %{y:,.0f}<extra></extra>"))
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(chart_layout(fig, 405), use_container_width=True)
    with col2:
        section("MX", "Revenue Mix", "Category contribution")
        cats = get_category_performance(filtered_df)
        fig = go.Figure(go.Pie(labels=cats["Category"], values=cats["Revenue"], hole=.58, marker=dict(colors=COLORS), hovertemplate="%{label}<br>Revenue: Rs %{value:,.0f}<extra></extra>"))
        fig.update_layout(**PLOTLY_LAYOUT, height=405, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        section("RG", "Regional Revenue")
        reg = get_regional_analysis(filtered_df)
        fig = go.Figure(go.Bar(x=reg["Region"], y=reg["Revenue"], marker=dict(color=reg["Revenue"], colorscale=[[0, COLORS[3]], [1, COLORS[0]]]), text=[money(v) for v in reg["Revenue"]], textposition="outside"))
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    with col4:
        section("PR", "Top Products")
        top = get_top_products(filtered_df, 10)
        fig = go.Figure(go.Bar(y=top["Product_Name"], x=top["Revenue"], orientation="h", marker=dict(color=top["Revenue"], colorscale=[[0, COLORS[5]], [1, COLORS[0]]]), text=[money(v) for v in top["Revenue"]], textposition="outside"))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

elif page == "Revenue & Trends":
    monthly = get_monthly_trends(filtered_df)
    yoy = get_yoy_growth(filtered_df)
    if len(yoy) > 1:
        cols = st.columns(4)
        latest, prev = yoy.iloc[-1], yoy.iloc[-2]
        with cols[0]: card(f"Revenue {int(latest['Year'])}", money(latest["Revenue"]), f"{latest['Revenue_Growth']:.1f}% YoY", COLORS[0])
        with cols[1]: card(f"Profit {int(latest['Year'])}", money(latest["Profit"]), f"{latest['Profit_Growth']:.1f}% YoY", COLORS[1])
        with cols[2]: card(f"Revenue {int(prev['Year'])}", money(prev["Revenue"]), f"{int(prev['Orders']):,} orders", COLORS[2])
        with cols[3]: card("Customers", f"{int(latest['Customers']):,}", "latest selected year", COLORS[4])
    section("TL", "Monthly and Cumulative Revenue")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"], y=monthly["Revenue"], name="Monthly", marker=dict(color=COLORS[0])), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Cumulative_Revenue"], name="Cumulative", line=dict(color=COLORS[2], width=3)), secondary_y=True)
    fig.update_xaxes(tickangle=-35)
    st.plotly_chart(chart_layout(fig, 430), use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        section("QR", "Quarterly Performance")
        q = get_seasonal_analysis(filtered_df)
        fig = go.Figure(go.Bar(x=q["Quarter_Label"], y=q["Revenue"], text=[money(v) for v in q["Revenue"]], textposition="outside", marker=dict(color=q["Profit_Margin"], colorscale=[[0, COLORS[3]], [1, COLORS[1]]])))
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    with col2:
        section("GR", "Monthly Growth")
        growth = monthly["Revenue_Growth"].fillna(0)
        fig = go.Figure(go.Bar(x=monthly["Month_Label"], y=growth, marker=dict(color=[COLORS[1] if v >= 0 else COLORS[3] for v in growth])))
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

elif page == "Regional Analysis":
    reg = get_regional_analysis(filtered_df)
    cols = st.columns(len(reg))
    for i, (_, row) in enumerate(reg.iterrows()):
        with cols[i]: card(row["Region"], money(row["Revenue"]), f"{row['Profit_Margin']:.1f}% margin", COLORS[i % len(COLORS)])
    section("HM", "Category Margin by Region")
    heat = get_profit_margin_heatmap_data(filtered_df)
    fig = go.Figure(go.Heatmap(z=heat.values, x=heat.columns, y=heat.index, text=[[f"{v:.1f}%" for v in row] for row in heat.values], texttemplate="%{text}", colorscale=[[0, COLORS[3]], [.5, COLORS[2]], [1, COLORS[1]]]))
    st.plotly_chart(chart_layout(fig, 390), use_container_width=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        section("CT", "Top Cities")
        cities = get_city_analysis(filtered_df, 15).copy()
        cities["Revenue"] = cities["Revenue"].apply(money)
        cities["Profit"] = cities["Profit"].apply(money)
        cities["Profit_Margin"] = cities["Profit_Margin"].map(lambda x: f"{x:.1f}%")
        st.dataframe(cities[["City", "State", "Region", "Revenue", "Profit", "Orders", "Profit_Margin"]], use_container_width=True, hide_index=True)
    with col2:
        section("3D", "City Category Revenue")
        matrix = get_3d_bar_data(filtered_df)
        fig = go.Figure()
        max_val = matrix.values.max() if matrix.size else 1
        for j, cat in enumerate(matrix.columns):
            for i, city in enumerate(matrix.index):
                value = matrix.loc[city, cat]
                if value > 0:
                    fig.add_trace(go.Scatter3d(x=[i], y=[j], z=[value], mode="markers", marker=dict(size=max(5, min(18, value / max_val * 18)), color=COLORS[j % len(COLORS)]), showlegend=False, hovertemplate=f"{city}<br>{cat}<br>Rs {value:,.0f}<extra></extra>"))
        fig.update_layout(**PLOTLY_LAYOUT, height=390, scene=dict(xaxis=dict(title="City", tickvals=list(range(len(matrix.index))), ticktext=matrix.index.tolist()), yaxis=dict(title="Category", tickvals=list(range(len(matrix.columns))), ticktext=matrix.columns.tolist()), zaxis=dict(title="Revenue")))
        st.plotly_chart(fig, use_container_width=True)

elif page == "Product Performance":
    col1, col2 = st.columns(2)
    with col1:
        section("UP", "Top 10 Products")
        top = get_top_products(filtered_df, 10)
        fig = go.Figure(go.Bar(y=top["Product_Name"], x=top["Revenue"], orientation="h", text=[money(v) for v in top["Revenue"]], textposition="outside", marker=dict(color=top["Profit_Margin"], colorscale=[[0, COLORS[3]], [1, COLORS[1]]])))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(chart_layout(fig, 405), use_container_width=True)
    with col2:
        section("DN", "Bottom 10 Products")
        bottom = get_top_products(filtered_df, 10, ascending=True)
        fig = go.Figure(go.Bar(y=bottom["Product_Name"], x=bottom["Revenue"], orientation="h", text=[money(v) for v in bottom["Revenue"]], textposition="outside", marker=dict(color=bottom["Profit_Margin"], colorscale=[[0, COLORS[3]], [1, COLORS[1]]])))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(chart_layout(fig, 405), use_container_width=True)
    section("TM", "Category and Sub-Category Treemap")
    sub = get_subcategory_performance(filtered_df)
    fig = px.treemap(sub, path=["Category", "Sub_Category"], values="Revenue", color="Profit_Margin", color_continuous_scale=[[0, COLORS[3]], [.5, COLORS[2]], [1, COLORS[1]]])
    fig.update_layout(**PLOTLY_LAYOUT, height=440)
    st.plotly_chart(fig, use_container_width=True)
    section("3D", "Product Quantity, Price, Profit")
    scatter = get_3d_scatter_data(filtered_df)
    fig = go.Figure()
    for idx, cat_name in enumerate(scatter["Category"].unique()):
        part = scatter[scatter["Category"] == cat_name]
        base = part["Revenue"].max() or 1
        fig.add_trace(go.Scatter3d(x=part["Quantity"], y=part["Avg_Price"], z=part["Profit"], mode="markers", name=cat_name, marker=dict(size=np.clip(part["Revenue"] / base * 16, 5, 20), color=COLORS[idx % len(COLORS)]), text=part["Product_Name"]))
    fig.update_layout(**PLOTLY_LAYOUT, height=510, scene=dict(xaxis=dict(title="Quantity"), yaxis=dict(title="Avg Price"), zaxis=dict(title="Profit")))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Customer Insights":
    seg = get_customer_segments(filtered_df)
    cols = st.columns(len(seg))
    for i, (_, row) in enumerate(seg.iterrows()):
        with cols[i]: card(row["Segment"], money(row["Revenue"]), f"{row['Revenue_Share']:.1f}% share", COLORS[i % len(COLORS)])
    col1, col2 = st.columns(2)
    with col1:
        section("PM", "Payment Mode")
        pay = get_payment_analysis(filtered_df)
        fig = go.Figure(go.Pie(labels=pay["Payment_Mode"], values=pay["Revenue"], hole=.55, marker=dict(colors=COLORS)))
        fig.update_layout(**PLOTLY_LAYOUT, height=390)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        section("SH", "Shipping Revenue")
        ship = get_shipping_analysis(filtered_df)
        fig = go.Figure(go.Bar(x=ship["Ship_Mode"], y=ship["Revenue"], text=[money(v) for v in ship["Revenue"]], textposition="outside", marker=dict(color=ship["Revenue"], colorscale=[[0, COLORS[5]], [1, COLORS[0]]])))
        st.plotly_chart(chart_layout(fig, 390), use_container_width=True)
    section("DC", "Discount Impact")
    corr = get_discount_profit_correlation(filtered_df)
    fig = px.scatter(corr, x="Discount", y="Avg_Profit", color="Category", size="Count", size_max=28, color_discrete_sequence=COLORS)
    fig.update_layout(**PLOTLY_LAYOUT, height=420, xaxis=dict(tickformat=".0%"))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Business Insights":
    section("IN", "Key Findings", "Generated from current filters")
    insights = generate_business_insights(filtered_df, kpis)
    cols = st.columns(2)
    accents = {"success": COLORS[1], "info": COLORS[0], "warning": COLORS[2], "danger": COLORS[3]}
    for i, item in enumerate(insights):
        with cols[i % 2]: insight_card(item["title"], item["text"], accents.get(item["type"], COLORS[0]), "IN")
    section("RC", "Strategic Recommendations", "Calculated from uploaded/current data")
    recs = get_strategic_recommendations(filtered_df)
    cols = st.columns(2)
    for i, item in enumerate(recs):
        with cols[i % 2]: rec_card(item["title"], item["text"], item["color"], "RC")
    section("DQ", "Data Source Check")
    qcols = st.columns(4)
    with qcols[0]: card("Filtered Rows", f"{filtered_quality['rows']:,}", f"from {source_label}", COLORS[0])
    with qcols[1]: card("Date Range", f"{filtered_quality['start_date'].strftime('%b %Y')} - {filtered_quality['end_date'].strftime('%b %Y')}", "based on Order_Date", COLORS[1])
    with qcols[2]: card("Products", f"{filtered_quality['products']:,}", "unique products", COLORS[2])
    with qcols[3]: card("Missing Values", f"{filtered_quality['missing_values']:,}", "after validation", COLORS[3])
    col1, col2 = st.columns(2)
    with col1: st.download_button("Download filtered data", filtered_df.to_csv(index=False), "sales_data_filtered.csv", "text/csv", use_container_width=True)
    with col2: st.download_button("Download category summary", get_category_performance(filtered_df).to_csv(index=False), "category_summary.csv", "text/csv", use_container_width=True)

st.markdown("<p class='small-note' style='text-align:center;margin-top:2rem'>Sales Data Analysis & Business Insights | Streamlit, Plotly, Pandas</p>", unsafe_allow_html=True)