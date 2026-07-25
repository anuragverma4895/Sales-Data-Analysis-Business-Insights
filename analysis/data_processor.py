"""
Data Processor — Analytics Engine
==================================
Core analysis functions for the Sales Data Analysis dashboard.
Provides KPI computation, trend analysis, regional breakdowns,
and business insight generation.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_and_clean_data(filepath="data/sales_data.csv"):
    """Load the sales CSV and perform cleaning/type conversions."""
    df = pd.read_csv(filepath)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Num"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Year"] = df["Order_Date"].dt.year
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()
    df["Week_Num"] = df["Order_Date"].dt.isocalendar().week.astype(int)
    df["Profit_Margin"] = np.where(df["Revenue"] > 0, (df["Profit"] / df["Revenue"]) * 100, 0)
    return df


def get_kpi_metrics(df):
    """Compute headline KPI metrics."""
    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_quantity = df["Quantity"].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    unique_customers = df["Customer_ID"].nunique()
    avg_discount = df["Discount"].mean() * 100

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "profit_margin": profit_margin,
        "unique_customers": unique_customers,
        "avg_discount": avg_discount,
    }


def get_monthly_trends(df):
    """Compute month-over-month revenue and profit trends."""
    monthly = (
        df.groupby(["Year", "Month_Num", "Month_Name"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values(["Year", "Month_Num"])
    )
    monthly["Month_Label"] = monthly["Month_Name"] + " " + monthly["Year"].astype(str)
    monthly["Revenue_Growth"] = monthly["Revenue"].pct_change() * 100
    monthly["Cumulative_Revenue"] = monthly["Revenue"].cumsum()
    return monthly


def get_category_performance(df):
    """Category-wise revenue, profit, quantity breakdown."""
    cat_perf = (
        df.groupby("Category")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Avg_Discount=("Discount", "mean"),
        )
        .reset_index()
    )
    cat_perf["Profit_Margin"] = (cat_perf["Profit"] / cat_perf["Revenue"] * 100).round(2)
    cat_perf["Revenue_Share"] = (cat_perf["Revenue"] / cat_perf["Revenue"].sum() * 100).round(2)
    cat_perf = cat_perf.sort_values("Revenue", ascending=False)
    return cat_perf


def get_subcategory_performance(df):
    """Sub-category level performance."""
    sub_perf = (
        df.groupby(["Category", "Sub_Category"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    sub_perf["Profit_Margin"] = (sub_perf["Profit"] / sub_perf["Revenue"] * 100).round(2)
    sub_perf = sub_perf.sort_values("Revenue", ascending=False)
    return sub_perf


def get_regional_analysis(df):
    """Region-wise & city-wise performance."""
    regional = (
        df.groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    regional["Profit_Margin"] = (regional["Profit"] / regional["Revenue"] * 100).round(2)
    regional = regional.sort_values("Revenue", ascending=False)
    return regional


def get_city_analysis(df, top_n=15):
    """City-level performance."""
    city = (
        df.groupby(["City", "State", "Region"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(top_n)
    )
    city["Profit_Margin"] = (city["Profit"] / city["Revenue"] * 100).round(2)
    return city


def get_seasonal_analysis(df):
    """Quarterly & seasonal pattern detection."""
    quarterly = (
        df.groupby(["Year", "Quarter"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
    )
    quarterly["Quarter_Label"] = "Q" + quarterly["Quarter"].astype(str) + " " + quarterly["Year"].astype(str)
    return quarterly


def get_customer_segments(df):
    """Segment-wise analysis (Consumer / Corporate / Home Office)."""
    segments = (
        df.groupby("Segment")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Customers=("Customer_ID", "nunique"),
            Avg_Order_Value=("Revenue", "mean"),
        )
        .reset_index()
    )
    segments["Profit_Margin"] = (segments["Profit"] / segments["Revenue"] * 100).round(2)
    segments["Revenue_Share"] = (segments["Revenue"] / segments["Revenue"].sum() * 100).round(2)
    return segments


def get_payment_analysis(df):
    """Payment mode distribution and revenue contribution."""
    payment = (
        df.groupby("Payment_Mode")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Order_ID", "nunique"),
            Avg_Order_Value=("Revenue", "mean"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    payment["Revenue_Share"] = (payment["Revenue"] / payment["Revenue"].sum() * 100).round(2)
    return payment


def get_top_products(df, n=10, metric="Revenue", ascending=False):
    """Top/Bottom N products by a given metric."""
    products = (
        df.groupby("Product_Name")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
        .sort_values(metric, ascending=ascending)
        .head(n)
    )
    products["Profit_Margin"] = (products["Profit"] / products["Revenue"] * 100).round(2)
    return products


def get_yoy_growth(df):
    """Year-over-Year growth comparison."""
    yearly = (
        df.groupby("Year")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Customers=("Customer_ID", "nunique"),
        )
        .reset_index()
    )
    yearly["Revenue_Growth"] = yearly["Revenue"].pct_change() * 100
    yearly["Profit_Growth"] = yearly["Profit"].pct_change() * 100
    return yearly


def get_profit_margin_heatmap_data(df):
    """Profit margin by Category × Region for heatmap."""
    heatmap = df.pivot_table(
        values="Profit_Margin",
        index="Category",
        columns="Region",
        aggfunc="mean",
    ).round(2)
    return heatmap


def get_3d_surface_data(df):
    """Revenue × Month × Category for 3D surface plot."""
    surface = df.pivot_table(
        values="Revenue",
        index="Month_Num",
        columns="Category",
        aggfunc="sum",
    ).fillna(0)
    return surface


def get_3d_scatter_data(df):
    """Prepare data for 3D scatter: Quantity × Unit_Price × Profit."""
    scatter = (
        df.groupby(["Product_Name", "Category", "Sub_Category"])
        .agg(
            Quantity=("Quantity", "sum"),
            Avg_Price=("Unit_Price", "mean"),
            Profit=("Profit", "sum"),
            Revenue=("Revenue", "sum"),
        )
        .reset_index()
    )
    return scatter


def get_3d_bar_data(df):
    """City × Category × Revenue for 3D bar chart."""
    bar_data = df.pivot_table(
        values="Revenue",
        index="City",
        columns="Category",
        aggfunc="sum",
    ).fillna(0)
    # Top 10 cities
    bar_data["Total"] = bar_data.sum(axis=1)
    bar_data = bar_data.sort_values("Total", ascending=False).head(10).drop("Total", axis=1)
    return bar_data


def get_discount_profit_correlation(df):
    """Discount vs Profit correlation data."""
    corr_data = (
        df.groupby(["Category", "Discount"])
        .agg(
            Avg_Profit=("Profit", "mean"),
            Avg_Revenue=("Revenue", "mean"),
            Count=("Order_ID", "count"),
        )
        .reset_index()
    )
    return corr_data


def get_shipping_analysis(df):
    """Shipping mode analysis."""
    shipping = (
        df.groupby("Ship_Mode")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Order_ID", "nunique"),
            Avg_Order_Value=("Revenue", "mean"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    shipping["Revenue_Share"] = (shipping["Revenue"] / shipping["Revenue"].sum() * 100).round(2)
    return shipping


def generate_business_insights(df, kpis):
    """Auto-generate key business insights from the data."""
    insights = []

    # 1. Top performing category
    cat_perf = get_category_performance(df)
    top_cat = cat_perf.iloc[0]
    insights.append({
        "icon": "trending_up",
        "title": "Top Revenue Category",
        "text": f"{top_cat['Category']} leads with ₹{top_cat['Revenue']:,.0f} in revenue, "
                f"contributing {top_cat['Revenue_Share']:.1f}% of total sales.",
        "type": "success",
    })

    # 2. Most profitable category
    most_profitable = cat_perf.sort_values("Profit_Margin", ascending=False).iloc[0]
    insights.append({
        "icon": "account_balance_wallet",
        "title": "Highest Profit Margin",
        "text": f"{most_profitable['Category']} has the highest profit margin at "
                f"{most_profitable['Profit_Margin']:.1f}%, making it the most efficient category.",
        "type": "info",
    })

    # 3. Regional insight
    regional = get_regional_analysis(df)
    top_region = regional.iloc[0]
    insights.append({
        "icon": "location_on",
        "title": "Strongest Region",
        "text": f"The {top_region['Region']} region dominates with ₹{top_region['Revenue']:,.0f} "
                f"revenue and {top_region['Orders']} orders.",
        "type": "success",
    })

    # 4. Seasonal peak
    monthly = get_monthly_trends(df)
    peak_month = monthly.loc[monthly["Revenue"].idxmax()]
    insights.append({
        "icon": "calendar_month",
        "title": "Peak Sales Month",
        "text": f"{peak_month['Month_Label']} recorded the highest revenue at "
                f"₹{peak_month['Revenue']:,.0f}, driven by festive season demand.",
        "type": "warning",
    })

    # 5. Customer segment
    segments = get_customer_segments(df)
    top_segment = segments.sort_values("Revenue", ascending=False).iloc[0]
    insights.append({
        "icon": "groups",
        "title": "Dominant Customer Segment",
        "text": f"{top_segment['Segment']} customers account for {top_segment['Revenue_Share']:.1f}% "
                f"of revenue with {top_segment['Customers']} unique customers.",
        "type": "info",
    })

    # 6. Discount impact
    high_disc = df[df["Discount"] >= 0.20]
    low_disc = df[df["Discount"] < 0.10]
    if len(high_disc) > 0 and len(low_disc) > 0:
        high_margin = high_disc["Profit_Margin"].mean()
        low_margin = low_disc["Profit_Margin"].mean()
        insights.append({
            "icon": "sell",
            "title": "Discount Impact Alert",
            "text": f"Orders with 20%+ discount average {high_margin:.1f}% margin vs "
                    f"{low_margin:.1f}% for orders under 10% discount. "
                    f"Deep discounting is eroding profits.",
            "type": "danger",
        })

    # 7. YoY Growth
    yoy = get_yoy_growth(df)
    if len(yoy) > 1 and not pd.isna(yoy.iloc[-1]["Revenue_Growth"]):
        growth = yoy.iloc[-1]["Revenue_Growth"]
        direction = "grew" if growth > 0 else "declined"
        insights.append({
            "icon": "show_chart",
            "title": "Year-over-Year Growth",
            "text": f"Revenue {direction} by {abs(growth):.1f}% in {int(yoy.iloc[-1]['Year'])} "
                    f"compared to {int(yoy.iloc[-2]['Year'])}.",
            "type": "success" if growth > 0 else "danger",
        })

    return insights
