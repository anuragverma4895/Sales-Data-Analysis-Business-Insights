"""
Sales Data Analysis & Business Insights
========================================
A professional-grade Streamlit dashboard with 3D interactive visualizations,
glass-morphism dark theme, and actionable business insights.

Author: Anurag Verma
Tech: Streamlit · Plotly · Pandas · NumPy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

from analysis.data_processor import (
    load_and_clean_data,
    get_kpi_metrics,
    get_monthly_trends,
    get_category_performance,
    get_subcategory_performance,
    get_regional_analysis,
    get_city_analysis,
    get_seasonal_analysis,
    get_customer_segments,
    get_payment_analysis,
    get_top_products,
    get_yoy_growth,
    get_profit_margin_heatmap_data,
    get_3d_surface_data,
    get_3d_scatter_data,
    get_3d_bar_data,
    get_discount_profit_correlation,
    get_shipping_analysis,
    generate_business_insights,
)

# ═══════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="Sales Analytics Dashboard | Anurag Verma",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load Custom CSS ──
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Material Icons CDN ──
st.markdown(
    '<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">',
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════
# PLOTLY THEME CONFIG
# ═══════════════════════════════════════════════

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#E2E8F0", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        bgcolor="rgba(26,31,46,0.7)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(size=11),
    ),
    hoverlabel=dict(
        bgcolor="#1A1F2E",
        bordercolor="rgba(255,255,255,0.1)",
        font=dict(family="Inter", size=12, color="#E2E8F0"),
    ),
)

COLOR_PALETTE = ["#667EEA", "#764BA2", "#F093FB", "#4FD1C5", "#34D399", "#FBBF24", "#FB7185", "#818CF8", "#A78BFA", "#F472B6"]
GRADIENT_COLORS = ["#667EEA", "#7C6BD6", "#9258C2", "#A845AE", "#BE329A", "#D41F86"]


def format_currency(value):
    """Format value to Indian currency style."""
    if abs(value) >= 1e7:
        return f"₹{value / 1e7:.2f} Cr"
    elif abs(value) >= 1e5:
        return f"₹{value / 1e5:.2f} L"
    elif abs(value) >= 1e3:
        return f"₹{value / 1e3:.1f} K"
    return f"₹{value:,.0f}"


def section_header(icon, title):
    """Render a styled section header with Material Icon."""
    st.markdown(
        f"""
        <div class="section-header">
            <span class="material-icons-round">{icon}</span>
            <h2>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_card(insight):
    """Render a styled insight card."""
    st.markdown(
        f"""
        <div class="insight-card {insight['type']}">
            <div class="insight-icon {insight['type']}">
                <span class="material-icons-round">{insight['icon']}</span>
            </div>
            <div>
                <div class="insight-title">{insight['title']}</div>
                <div class="insight-text">{insight['text']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════

@st.cache_data
def load_data():
    """Load and cache the sales data."""
    return load_and_clean_data()


df = load_data()

# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
            <span class="material-icons-round" style="font-size:2.5rem; background: linear-gradient(135deg, #667EEA, #764BA2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">analytics</span>
            <h1 style="margin:0.3rem 0 0 0; font-size:1.2rem;">Sales Analytics</h1>
            <p style="color:#64748B; font-size:0.75rem; margin:0;">Business Intelligence Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Page navigation
    st.markdown("## Navigation")
    page = st.radio(
        "Select Page",
        [
            "Overview",
            "Revenue & Trends",
            "Regional Analysis",
            "Product Performance",
            "Customer Insights",
            "Business Insights",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Filters
    st.markdown("## Filters")

    # Year filter
    years = sorted(df["Year"].unique())
    selected_years = st.multiselect("Year", years, default=years)

    # Region filter
    regions = sorted(df["Region"].unique())
    selected_regions = st.multiselect("Region", regions, default=regions)

    # Category filter
    categories = sorted(df["Category"].unique())
    selected_categories = st.multiselect("Category", categories, default=categories)

    # Segment filter
    segments = sorted(df["Segment"].unique())
    selected_segments = st.multiselect("Segment", segments, default=segments)

    st.markdown("---")

    # Data info
    st.markdown(
        f"""
        <div style="text-align:center; padding:0.5rem; background:rgba(102,126,234,0.08); border-radius:12px; border:1px solid rgba(102,126,234,0.15);">
            <span class="material-icons-round" style="font-size:1.2rem; color:#667EEA;">storage</span>
            <p style="margin:0.3rem 0 0 0; font-size:0.75rem; color:#94A3B8;">
                <strong style="color:#E2E8F0;">{len(df):,}</strong> records loaded<br>
                {df['Order_Date'].min().strftime('%b %Y')} — {df['Order_Date'].max().strftime('%b %Y')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Apply Filters ──
filtered_df = df[
    (df["Year"].isin(selected_years))
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Segment"].isin(selected_segments))
]

if filtered_df.empty:
    st.warning("No data matches the current filter selection. Please adjust the filters.")
    st.stop()

# Pre-compute metrics
kpis = get_kpi_metrics(filtered_df)

# ═══════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════

if page == "Overview":
    # Header
    st.markdown(
        """
        <div style="text-align:center; padding:1rem 0 0.5rem 0;">
            <h1 style="font-size:2.4rem; margin-bottom:0.3rem;">Sales Analytics Dashboard</h1>
            <p style="color:#94A3B8; font-size:0.95rem; font-weight:400;">
                Real-time business intelligence · Revenue trends · Customer behavior · Actionable insights
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ── KPI Row ──
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric(
            label="Total Revenue",
            value=format_currency(kpis["total_revenue"]),
            delta=f"{kpis['total_orders']:,} orders",
        )
    with kpi_cols[1]:
        st.metric(
            label="Total Profit",
            value=format_currency(kpis["total_profit"]),
            delta=f"{kpis['profit_margin']:.1f}% margin",
        )
    with kpi_cols[2]:
        st.metric(
            label="Avg Order Value",
            value=format_currency(kpis["avg_order_value"]),
            delta=f"{kpis['total_quantity']:,} units sold",
        )
    with kpi_cols[3]:
        st.metric(
            label="Unique Customers",
            value=f"{kpis['unique_customers']:,}",
            delta=f"{kpis['avg_discount']:.1f}% avg discount",
        )

    st.markdown("")

    # ── Revenue Trend + Category Donut ──
    col1, col2 = st.columns([2, 1])

    with col1:
        section_header("trending_up", "Revenue Trend")
        monthly = get_monthly_trends(filtered_df)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["Month_Label"],
            y=monthly["Revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color="#667EEA", width=3, shape="spline"),
            marker=dict(size=6, color="#667EEA"),
            fill="tonexty" if len(monthly) > 2 else None,
            fillcolor="rgba(102,126,234,0.08)",
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=monthly["Month_Label"],
            y=monthly["Profit"],
            mode="lines+markers",
            name="Profit",
            line=dict(color="#34D399", width=2, dash="dot", shape="spline"),
            marker=dict(size=5, color="#34D399"),
            hovertemplate="<b>%{x}</b><br>Profit: ₹%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=None,
            height=380,
            xaxis=dict(
                showgrid=False,
                tickangle=-45,
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.04)",
                tickformat=",",
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("donut_large", "Revenue by Category")
        cat_perf = get_category_performance(filtered_df)

        fig = go.Figure(data=[go.Pie(
            labels=cat_perf["Category"],
            values=cat_perf["Revenue"],
            hole=0.55,
            marker=dict(colors=COLOR_PALETTE[:len(cat_perf)]),
            textinfo="label+percent",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=None,
            height=380,
            showlegend=False,
            annotations=[dict(
                text=format_currency(kpis["total_revenue"]),
                x=0.5, y=0.5,
                font=dict(size=16, color="#E2E8F0", family="Outfit"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Regional Performance + Top Products ──
    col3, col4 = st.columns(2)

    with col3:
        section_header("map", "Regional Performance")
        regional = get_regional_analysis(filtered_df)

        fig = go.Figure(data=[go.Bar(
            x=regional["Region"],
            y=regional["Revenue"],
            marker=dict(
                color=regional["Revenue"],
                colorscale=[[0, "#667EEA"], [0.5, "#764BA2"], [1, "#F093FB"]],
                cornerradius=6,
            ),
            text=[format_currency(v) for v in regional["Revenue"]],
            textposition="outside",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=None,
            height=350,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        section_header("inventory_2", "Top 10 Products by Revenue")
        top_products = get_top_products(filtered_df, n=10, metric="Revenue")

        fig = go.Figure(data=[go.Bar(
            y=top_products["Product_Name"],
            x=top_products["Revenue"],
            orientation="h",
            marker=dict(
                color=top_products["Revenue"],
                colorscale=[[0, "#4FD1C5"], [0.5, "#667EEA"], [1, "#764BA2"]],
                cornerradius=4,
            ),
            text=[format_currency(v) for v in top_products["Revenue"]],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=None,
            height=350,
            yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: REVENUE & TRENDS
# ═══════════════════════════════════════════════

elif page == "Revenue & Trends":
    st.markdown('<h1 style="text-align:center;">Revenue & Trends Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;">Deep dive into revenue patterns, seasonal trends, and year-over-year growth</p>', unsafe_allow_html=True)
    st.markdown("")

    monthly = get_monthly_trends(filtered_df)
    yoy = get_yoy_growth(filtered_df)

    # ── YoY KPIs ──
    if len(yoy) > 1:
        yoy_cols = st.columns(4)
        latest = yoy.iloc[-1]
        prev = yoy.iloc[-2]
        with yoy_cols[0]:
            st.metric(f"Revenue {int(latest['Year'])}", format_currency(latest["Revenue"]),
                      delta=f"{latest['Revenue_Growth']:.1f}% YoY" if not pd.isna(latest["Revenue_Growth"]) else "N/A")
        with yoy_cols[1]:
            st.metric(f"Profit {int(latest['Year'])}", format_currency(latest["Profit"]),
                      delta=f"{latest['Profit_Growth']:.1f}% YoY" if not pd.isna(latest["Profit_Growth"]) else "N/A")
        with yoy_cols[2]:
            st.metric(f"Revenue {int(prev['Year'])}", format_currency(prev["Revenue"]))
        with yoy_cols[3]:
            st.metric(f"Profit {int(prev['Year'])}", format_currency(prev["Profit"]))

    st.markdown("")

    # ── Monthly Revenue with Cumulative ──
    section_header("show_chart", "Monthly Revenue & Cumulative Growth")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=monthly["Month_Label"],
            y=monthly["Revenue"],
            name="Monthly Revenue",
            marker=dict(
                color=monthly["Revenue"],
                colorscale=[[0, "#667EEA"], [1, "#764BA2"]],
                cornerradius=4,
            ),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=monthly["Month_Label"],
            y=monthly["Cumulative_Revenue"],
            name="Cumulative Revenue",
            line=dict(color="#FBBF24", width=3, shape="spline"),
            mode="lines",
            hovertemplate="<b>%{x}</b><br>Cumulative: ₹%{y:,.0f}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=420,
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=",", title="Monthly Revenue"),
        yaxis2=dict(showgrid=False, tickformat=",", title="Cumulative"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── 3D Surface: Revenue × Month × Category ──
    section_header("view_in_ar", "3D Revenue Surface — Month × Category")

    surface_data = get_3d_surface_data(filtered_df)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    categories_list = surface_data.columns.tolist()

    fig = go.Figure(data=[go.Surface(
        z=surface_data.values,
        x=list(range(len(categories_list))),
        y=surface_data.index.tolist(),
        colorscale=[
            [0, "#0E1117"],
            [0.2, "#1A1F3D"],
            [0.4, "#667EEA"],
            [0.6, "#764BA2"],
            [0.8, "#F093FB"],
            [1, "#FB7185"],
        ],
        contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True),
        ),
        opacity=0.92,
        hovertemplate="Category: %{x}<br>Month: %{y}<br>Revenue: ₹%{z:,.0f}<extra></extra>",
    )])
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=550,
        scene=dict(
            xaxis=dict(
                title="Category",
                tickvals=list(range(len(categories_list))),
                ticktext=categories_list,
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.06)",
                color="#94A3B8",
            ),
            yaxis=dict(
                title="Month",
                tickvals=list(range(1, 13)),
                ticktext=month_names,
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.06)",
                color="#94A3B8",
            ),
            zaxis=dict(
                title="Revenue (₹)",
                backgroundcolor="rgba(0,0,0,0)",
                gridcolor="rgba(255,255,255,0.06)",
                color="#94A3B8",
            ),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Seasonal / Quarterly Analysis ──
    col1, col2 = st.columns(2)

    with col1:
        section_header("calendar_month", "Quarterly Performance")
        quarterly = get_seasonal_analysis(filtered_df)

        fig = go.Figure(data=[go.Bar(
            x=quarterly["Quarter_Label"],
            y=quarterly["Revenue"],
            marker=dict(
                color=quarterly["Revenue"],
                colorscale=[[0, "#4FD1C5"], [0.5, "#667EEA"], [1, "#F093FB"]],
                cornerradius=6,
            ),
            text=[format_currency(v) for v in quarterly["Revenue"]],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=350,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("waterfall_chart", "Monthly Growth Rate")

        fig = go.Figure(data=[go.Bar(
            x=monthly["Month_Label"],
            y=monthly["Revenue_Growth"].fillna(0),
            marker=dict(
                color=[
                    "#34D399" if v >= 0 else "#FB7185"
                    for v in monthly["Revenue_Growth"].fillna(0)
                ],
                cornerradius=4,
            ),
            hovertemplate="<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=350,
            xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", title="Growth %"),
        )
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: REGIONAL ANALYSIS
# ═══════════════════════════════════════════════

elif page == "Regional Analysis":
    st.markdown('<h1 style="text-align:center;">Regional Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;">Geographic breakdown of sales performance across India</p>', unsafe_allow_html=True)
    st.markdown("")

    regional = get_regional_analysis(filtered_df)
    city_data = get_city_analysis(filtered_df, top_n=15)

    # ── Region KPIs ──
    reg_cols = st.columns(len(regional))
    region_colors = {"North": "#667EEA", "South": "#34D399", "West": "#FBBF24", "East": "#FB7185"}
    for i, row in regional.iterrows():
        with reg_cols[list(regional.index).index(i)]:
            color = region_colors.get(row["Region"], "#667EEA")
            st.markdown(
                f"""
                <div style="background:rgba(26,31,46,0.65); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.08);
                            border-radius:16px; padding:1.2rem; text-align:center; border-top:3px solid {color};">
                    <p style="color:#94A3B8; font-size:0.8rem; margin:0; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">
                        {row['Region']} Region
                    </p>
                    <p style="font-family:Outfit; font-size:1.5rem; font-weight:800; color:#E2E8F0; margin:0.4rem 0;">
                        {format_currency(row['Revenue'])}
                    </p>
                    <p style="color:{color}; font-size:0.8rem; margin:0;">{row['Profit_Margin']:.1f}% margin · {row['Orders']} orders</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    # ── 3D Bar Chart: City × Category × Revenue ──
    section_header("view_in_ar", "3D City Performance — Revenue by Category")

    bar_3d = get_3d_bar_data(filtered_df)
    cities_list = bar_3d.index.tolist()
    cat_list = bar_3d.columns.tolist()

    fig = go.Figure()
    for j, cat in enumerate(cat_list):
        for i, city in enumerate(cities_list):
            val = bar_3d.loc[city, cat]
            if val > 0:
                fig.add_trace(go.Scatter3d(
                    x=[i], y=[j], z=[val],
                    mode="markers",
                    marker=dict(
                        size=max(4, min(18, val / bar_3d.values.max() * 18)),
                        color=COLOR_PALETTE[j % len(COLOR_PALETTE)],
                        opacity=0.85,
                        symbol="diamond",
                    ),
                    name=f"{city} - {cat}",
                    showlegend=False,
                    hovertemplate=f"<b>{city}</b><br>{cat}<br>Revenue: ₹{val:,.0f}<extra></extra>",
                ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=550,
        scene=dict(
            xaxis=dict(title="City", tickvals=list(range(len(cities_list))), ticktext=cities_list,
                       backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            yaxis=dict(title="Category", tickvals=list(range(len(cat_list))), ticktext=cat_list,
                       backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            zaxis=dict(title="Revenue (₹)", backgroundcolor="rgba(0,0,0,0)",
                       gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=2.0, y=1.5, z=1.0)),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── City Performance Table + Radar Chart ──
    col1, col2 = st.columns([1.2, 1])

    with col1:
        section_header("apartment", "Top Cities by Revenue")
        city_display = city_data[["City", "State", "Region", "Revenue", "Profit", "Orders", "Profit_Margin"]].copy()
        city_display["Revenue"] = city_display["Revenue"].apply(lambda x: f"₹{x:,.0f}")
        city_display["Profit"] = city_display["Profit"].apply(lambda x: f"₹{x:,.0f}")
        city_display["Profit_Margin"] = city_display["Profit_Margin"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(city_display, use_container_width=True, hide_index=True)

    with col2:
        section_header("radar", "Region Comparison — Radar")
        radar_cats = ["Revenue", "Profit", "Orders", "Quantity"]

        fig = go.Figure()
        for _, row in regional.iterrows():
            values = [
                row["Revenue"] / regional["Revenue"].max(),
                row["Profit"] / regional["Profit"].max(),
                row["Orders"] / regional["Orders"].max(),
                row["Quantity"] / regional["Quantity"].max(),
            ]
            values.append(values[0])  # Close the polygon
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=radar_cats + [radar_cats[0]],
                name=row["Region"],
                line=dict(color=region_colors.get(row["Region"], "#667EEA"), width=2),
                fill="toself",
                fillcolor=region_colors.get(row["Region"], "#667EEA").replace(")", ",0.1)").replace("rgb", "rgba") if "rgb" in region_colors.get(row["Region"], "") else f"rgba(102,126,234,0.1)",
                opacity=0.8,
            ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=400,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 1.1], showticklabels=False, gridcolor="rgba(255,255,255,0.06)"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: PRODUCT PERFORMANCE
# ═══════════════════════════════════════════════

elif page == "Product Performance":
    st.markdown('<h1 style="text-align:center;">Product Performance</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;">Product-level analysis, category breakdown, and pricing insights</p>', unsafe_allow_html=True)
    st.markdown("")

    # ── Top & Bottom Products ──
    col1, col2 = st.columns(2)

    with col1:
        section_header("trending_up", "Top 10 Products — Revenue")
        top_10 = get_top_products(filtered_df, n=10, metric="Revenue")

        fig = go.Figure(data=[go.Bar(
            y=top_10["Product_Name"],
            x=top_10["Revenue"],
            orientation="h",
            marker=dict(
                color=top_10["Revenue"],
                colorscale=[[0, "#34D399"], [0.5, "#4FD1C5"], [1, "#667EEA"]],
                cornerradius=4,
            ),
            text=[format_currency(v) for v in top_10["Revenue"]],
            textposition="outside",
            textfont=dict(size=9, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT, height=400,
            yaxis=dict(autorange="reversed", tickfont=dict(size=9)),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("trending_down", "Bottom 10 Products — Revenue")
        bottom_10 = get_top_products(filtered_df, n=10, metric="Revenue", ascending=True)

        fig = go.Figure(data=[go.Bar(
            y=bottom_10["Product_Name"],
            x=bottom_10["Revenue"],
            orientation="h",
            marker=dict(
                color=bottom_10["Revenue"],
                colorscale=[[0, "#FB7185"], [0.5, "#F093FB"], [1, "#764BA2"]],
                cornerradius=4,
            ),
            text=[format_currency(v) for v in bottom_10["Revenue"]],
            textposition="outside",
            textfont=dict(size=9, color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT, height=400,
            yaxis=dict(autorange="reversed", tickfont=dict(size=9)),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Category Treemap ──
    section_header("account_tree", "Category & Sub-Category Treemap")
    sub_perf = get_subcategory_performance(filtered_df)

    fig = px.treemap(
        sub_perf,
        path=["Category", "Sub_Category"],
        values="Revenue",
        color="Profit_Margin",
        color_continuous_scale=[[0, "#FB7185"], [0.3, "#764BA2"], [0.5, "#667EEA"], [0.7, "#4FD1C5"], [1, "#34D399"]],
        color_continuous_midpoint=sub_perf["Profit_Margin"].median(),
        hover_data={"Revenue": ":,.0f", "Profit": ":,.0f", "Profit_Margin": ":.1f"},
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=450,
        coloraxis_colorbar=dict(title="Margin %", tickfont=dict(color="#94A3B8"), titlefont=dict(color="#94A3B8")),
    )
    fig.update_traces(
        textfont=dict(color="#E2E8F0", size=12),
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Margin: %{color:.1f}%<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── 3D Scatter: Quantity × Price × Profit ──
    section_header("bubble_chart", "3D Product Analysis — Quantity × Price × Profit")

    scatter_data = get_3d_scatter_data(filtered_df)

    fig = go.Figure()
    for cat in scatter_data["Category"].unique():
        cat_df = scatter_data[scatter_data["Category"] == cat]
        idx = list(scatter_data["Category"].unique()).index(cat)
        fig.add_trace(go.Scatter3d(
            x=cat_df["Quantity"],
            y=cat_df["Avg_Price"],
            z=cat_df["Profit"],
            mode="markers",
            name=cat,
            marker=dict(
                size=np.clip(cat_df["Revenue"] / cat_df["Revenue"].max() * 16, 4, 20),
                color=COLOR_PALETTE[idx % len(COLOR_PALETTE)],
                opacity=0.8,
                line=dict(width=1, color="rgba(255,255,255,0.2)"),
            ),
            text=cat_df["Product_Name"],
            hovertemplate="<b>%{text}</b><br>Qty: %{x}<br>Avg Price: ₹%{y:,.0f}<br>Profit: ₹%{z:,.0f}<extra></extra>",
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=550,
        scene=dict(
            xaxis=dict(title="Quantity Sold", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            yaxis=dict(title="Avg Unit Price (₹)", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            zaxis=dict(title="Total Profit (₹)", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.2)),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: CUSTOMER INSIGHTS
# ═══════════════════════════════════════════════

elif page == "Customer Insights":
    st.markdown('<h1 style="text-align:center;">Customer Insights</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;">Customer segmentation, payment behavior, and purchasing patterns</p>', unsafe_allow_html=True)
    st.markdown("")

    segments = get_customer_segments(filtered_df)
    payment = get_payment_analysis(filtered_df)

    # ── Segment KPIs ──
    seg_cols = st.columns(len(segments))
    seg_colors = {"Consumer": "#667EEA", "Corporate": "#34D399", "Home Office": "#FBBF24"}
    for i, (_, row) in enumerate(segments.iterrows()):
        with seg_cols[i]:
            color = seg_colors.get(row["Segment"], "#667EEA")
            st.markdown(
                f"""
                <div style="background:rgba(26,31,46,0.65); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.08);
                            border-radius:16px; padding:1.2rem; text-align:center; border-top:3px solid {color};">
                    <p style="color:#94A3B8; font-size:0.75rem; margin:0; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">
                        {row['Segment']}
                    </p>
                    <p style="font-family:Outfit; font-size:1.4rem; font-weight:800; color:#E2E8F0; margin:0.3rem 0;">
                        {format_currency(row['Revenue'])}
                    </p>
                    <p style="color:{color}; font-size:0.75rem; margin:0;">
                        {row['Revenue_Share']:.1f}% share · {row['Customers']} customers · {row['Profit_Margin']:.1f}% margin
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    # ── Payment + Shipping ──
    col1, col2 = st.columns(2)

    with col1:
        section_header("payments", "Payment Mode Distribution")

        fig = go.Figure(data=[go.Pie(
            labels=payment["Payment_Mode"],
            values=payment["Revenue"],
            hole=0.5,
            marker=dict(colors=COLOR_PALETTE[:len(payment)]),
            textinfo="label+percent",
            textfont=dict(size=11, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=380,
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("local_shipping", "Shipping Mode Analysis")
        shipping = get_shipping_analysis(filtered_df)

        fig = go.Figure(data=[go.Bar(
            x=shipping["Ship_Mode"],
            y=shipping["Revenue"],
            marker=dict(
                color=shipping["Revenue"],
                colorscale=[[0, "#4FD1C5"], [1, "#667EEA"]],
                cornerradius=6,
            ),
            text=[f"{format_currency(v)}\n({s:.0f}%)" for v, s in zip(shipping["Revenue"], shipping["Revenue_Share"])],
            textposition="outside",
            textfont=dict(size=10, color="#94A3B8"),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=380,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── 3D Bubble: Segments × Revenue × Profit ──
    section_header("view_in_ar", "3D Customer Segment Analysis")

    seg_data = filtered_df.groupby(["Segment", "Category"]).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique"),
    ).reset_index()

    fig = go.Figure()
    for seg in seg_data["Segment"].unique():
        seg_df = seg_data[seg_data["Segment"] == seg]
        color = seg_colors.get(seg, "#667EEA")
        fig.add_trace(go.Scatter3d(
            x=seg_df["Revenue"],
            y=seg_df["Profit"],
            z=seg_df["Orders"],
            mode="markers+text",
            name=seg,
            marker=dict(
                size=np.clip(seg_df["Revenue"] / seg_df["Revenue"].max() * 18, 6, 22),
                color=color,
                opacity=0.8,
                line=dict(width=1, color="rgba(255,255,255,0.2)"),
            ),
            text=seg_df["Category"],
            textfont=dict(size=8, color="#94A3B8"),
            hovertemplate=f"<b>{seg}</b><br>%{{text}}<br>Revenue: ₹%{{x:,.0f}}<br>Profit: ₹%{{y:,.0f}}<br>Orders: %{{z}}<extra></extra>",
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=520,
        scene=dict(
            xaxis=dict(title="Revenue (₹)", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            yaxis=dict(title="Profit (₹)", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            zaxis=dict(title="Orders", backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)", color="#94A3B8"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Discount vs Profit ──
    section_header("sell", "Discount Impact on Profitability")

    corr = get_discount_profit_correlation(filtered_df)

    fig = px.scatter(
        corr,
        x="Discount",
        y="Avg_Profit",
        color="Category",
        size="Count",
        size_max=25,
        color_discrete_sequence=COLOR_PALETTE,
        hover_data={"Avg_Revenue": ":,.0f", "Count": True},
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=400,
        xaxis=dict(title="Discount %", showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=".0%"),
        yaxis=dict(title="Avg Profit (₹)", showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickformat=","),
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="rgba(255,255,255,0.15)")),
        hovertemplate="<b>%{customdata[0]}</b><br>Discount: %{x:.0%}<br>Avg Profit: ₹%{y:,.0f}<br>Orders: %{marker.size}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: BUSINESS INSIGHTS
# ═══════════════════════════════════════════════

elif page == "Business Insights":
    st.markdown('<h1 style="text-align:center;">Business Insights & Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94A3B8;">AI-generated insights derived from comprehensive data analysis</p>', unsafe_allow_html=True)
    st.markdown("")

    # ── Key Findings ──
    section_header("lightbulb", "Key Findings")
    insights = generate_business_insights(filtered_df, kpis)

    insight_cols = st.columns(2)
    for i, insight in enumerate(insights):
        with insight_cols[i % 2]:
            render_insight_card(insight)

    st.markdown("")

    # ── Profit Margin Heatmap ──
    section_header("grid_on", "Profit Margin Heatmap — Category × Region")

    heatmap_data = get_profit_margin_heatmap_data(filtered_df)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns.tolist(),
        y=heatmap_data.index.tolist(),
        colorscale=[
            [0, "#FB7185"],
            [0.3, "#764BA2"],
            [0.5, "#667EEA"],
            [0.7, "#4FD1C5"],
            [1, "#34D399"],
        ],
        text=[[f"{v:.1f}%" for v in row] for row in heatmap_data.values],
        texttemplate="%{text}",
        textfont=dict(size=13, color="#E2E8F0"),
        hovertemplate="<b>%{y}</b> — %{x}<br>Margin: %{z:.1f}%<extra></extra>",
        colorbar=dict(
            title="Margin %",
            tickfont=dict(color="#94A3B8"),
            titlefont=dict(color="#94A3B8"),
        ),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        xaxis=dict(side="top"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Strategic Recommendations ──
    section_header("tips_and_updates", "Strategic Recommendations")

    recommendations = [
        {
            "icon": "rocket_launch",
            "title": "Double Down on Festive Season",
            "text": "Q4 (Oct-Nov) shows 30-40% revenue surge. Increase inventory and marketing spend 6 weeks before Diwali to maximize returns.",
            "color": "#667EEA",
        },
        {
            "icon": "precision_manufacturing",
            "title": "Optimize Discount Strategy",
            "text": "Discounts above 20% significantly erode margins. Cap maximum discounts at 20% and use bundled offers instead of deep cuts.",
            "color": "#FBBF24",
        },
        {
            "icon": "groups",
            "title": "Expand Corporate Segment",
            "text": "Corporate customers show higher AOV and consistent purchasing. Launch dedicated B2B programs with volume-based pricing.",
            "color": "#34D399",
        },
        {
            "icon": "inventory_2",
            "title": "Focus on High-Margin Categories",
            "text": "Accessories and supplies categories have the best margins. Cross-sell these with high-ticket items to improve overall profitability.",
            "color": "#4FD1C5",
        },
        {
            "icon": "location_on",
            "title": "Strengthen East Region",
            "text": "Eastern India shows untapped potential with lower penetration. Invest in regional marketing and fulfillment infrastructure.",
            "color": "#FB7185",
        },
        {
            "icon": "smartphone",
            "title": "Promote Digital Payments",
            "text": "UPI is the dominant payment mode. Offer cashback incentives on digital payments to reduce cash handling costs.",
            "color": "#A78BFA",
        },
    ]

    rec_cols = st.columns(2)
    for i, rec in enumerate(recommendations):
        with rec_cols[i % 2]:
            st.markdown(
                f"""
                <div style="background:rgba(26,31,46,0.65); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.08);
                            border-radius:16px; padding:1.2rem 1.4rem; margin-bottom:0.8rem; border-left:4px solid {rec['color']};">
                    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
                        <span class="material-icons-round" style="color:{rec['color']}; font-size:1.3rem;">{rec['icon']}</span>
                        <span style="font-family:Outfit; font-weight:700; font-size:0.95rem; color:#E2E8F0;">{rec['title']}</span>
                    </div>
                    <p style="color:#94A3B8; font-size:0.85rem; line-height:1.5; margin:0;">{rec['text']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    # ── Data Export ──
    section_header("download", "Export Data")
    col1, col2 = st.columns(2)
    with col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_data,
            file_name="sales_data_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col2:
        summary_data = get_category_performance(filtered_df).to_csv(index=False)
        st.download_button(
            label="Download Category Summary (CSV)",
            data=summary_data,
            file_name="category_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════

st.markdown(
    """
    <div class="footer">
        <p>
            <span class="material-icons-round" style="font-size:1rem; vertical-align:middle; color:#667EEA;">analytics</span>
            Sales Data Analysis & Business Insights · Built by <strong>Anurag Verma</strong>
        </p>
        <p style="font-size:0.7rem; color:#475569;">
            Streamlit · Plotly · Pandas · NumPy · Python
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
