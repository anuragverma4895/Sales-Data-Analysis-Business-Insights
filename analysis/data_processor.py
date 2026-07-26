"""
Data Processor - Analytics Engine
=================================
Core analysis functions for the Sales Data Analysis dashboard.
All dashboard values are calculated from data/sales_data.csv.
"""

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Customer_Name",
    "Segment",
    "City",
    "State",
    "Region",
    "Category",
    "Sub_Category",
    "Product_Name",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Revenue",
    "Profit",
    "Payment_Mode",
    "Ship_Mode",
}

NUMERIC_COLUMNS = ["Quantity", "Unit_Price", "Discount", "Revenue", "Profit"]
COLUMN_ALIASES = {
    "Order_ID": ["order id", "order_id", "orderid", "order no", "order number", "invoice id", "invoice no", "invoice number"],
    "Order_Date": ["order date", "order_date", "date", "invoice date", "purchase date", "transaction date"],
    "Customer_ID": ["customer id", "customer_id", "customerid", "client id", "buyer id"],
    "Customer_Name": ["customer name", "customer_name", "customer", "client", "buyer name", "name"],
    "Segment": ["segment", "customer segment", "market segment", "sales channel", "channel", "order priority"],
    "City": ["city", "town"],
    "State": ["state", "province", "country"],
    "Region": ["region", "zone", "area"],
    "Category": ["category", "product category", "item category", "item type", "itemtype"],
    "Sub_Category": ["sub-category", "sub_category", "subcategory", "sub category", "product sub-category", "item type", "itemtype"],
    "Product_Name": ["product name", "product_name", "product", "item", "item name", "sku name", "item type", "itemtype"],
    "Quantity": ["quantity", "qty", "units", "unit sold", "units sold"],
    "Unit_Price": ["unit price", "unit_price", "price", "selling price", "rate", "unit cost"],
    "Discount": ["discount", "discount %", "discount percent", "discount rate"],
    "Revenue": ["revenue", "sales", "amount", "total", "total sales", "sales amount", "net sales", "total revenue", "gross sales"],
    "Profit": ["profit", "gross profit", "net profit", "margin amount", "total profit"],
    "Payment_Mode": ["payment mode", "payment_mode", "payment", "payment method", "mode of payment"],
    "Ship_Mode": ["ship mode", "ship_mode", "shipping mode", "delivery mode", "shipment mode"],
}

OPTIONAL_DEFAULTS = {
    "Customer_ID": "Unknown Customer",
    "Customer_Name": "Unknown Customer",
    "Segment": "Unspecified",
    "City": "Unspecified",
    "State": "Unspecified",
    "Region": "Unspecified",
    "Category": "Uncategorized",
    "Sub_Category": "Uncategorized",
    "Product_Name": "Unknown Product",
    "Quantity": 1,
    "Unit_Price": 0,
    "Discount": 0,
    "Profit": 0,
    "Payment_Mode": "Unspecified",
    "Ship_Mode": "Unspecified",
}


def _normalize_column_name(name):
    return " ".join(str(name).strip().lower().replace("_", " ").replace("-", " ").split())


def _standardize_columns(df):
    normalized = {_normalize_column_name(col): col for col in df.columns}
    rename_map = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        keys = [_normalize_column_name(canonical), *[_normalize_column_name(alias) for alias in aliases]]
        for key in keys:
            if key in normalized:
                rename_map[normalized[key]] = canonical
                break
    df = df.rename(columns=rename_map)
    if "Profit" not in df.columns and {"Revenue", "Total Cost"}.issubset(df.columns):
        df["Profit"] = pd.to_numeric(df["Revenue"], errors="coerce") - pd.to_numeric(df["Total Cost"], errors="coerce")
    if "Category" not in df.columns and "Product_Name" in df.columns:
        df["Category"] = df["Product_Name"]
    if "Product_Name" not in df.columns and "Category" in df.columns:
        df["Product_Name"] = df["Category"]
    return df


def _fill_optional_columns(df):
    for column, default in OPTIONAL_DEFAULTS.items():
        if column not in df.columns:
            if column == "Unit_Price" and {"Revenue", "Quantity"}.issubset(df.columns):
                quantity = pd.to_numeric(df["Quantity"], errors="coerce").replace(0, np.nan)
                df[column] = pd.to_numeric(df["Revenue"], errors="coerce") / quantity
            else:
                df[column] = default
    return df


def _safe_pct(numerator, denominator):
    return np.where(denominator != 0, (numerator / denominator) * 100, 0)


def _format_money(value):
    value = float(value) if pd.notna(value) else 0.0
    if abs(value) >= 1e7:
        return f"Rs {value / 1e7:.2f} Cr"
    if abs(value) >= 1e5:
        return f"Rs {value / 1e5:.2f} L"
    if abs(value) >= 1e3:
        return f"Rs {value / 1e3:.1f} K"
    return f"Rs {value:,.0f}"


def load_and_clean_data(filepath=None):
    """Load the sales CSV and perform validation/type conversions."""
    if filepath is None:
        filepath = Path(__file__).resolve().parents[1] / "data" / "sales_data.csv"

    if isinstance(filepath, pd.DataFrame):
        df = filepath.copy()
    else:
        df = pd.read_csv(filepath)
    df = _standardize_columns(df)

    required_core = {"Order_ID", "Order_Date", "Revenue"}
    missing_core = required_core.difference(df.columns)
    if missing_core:
        missing = ", ".join(sorted(missing_core))
        available = ", ".join(map(str, df.columns))
        raise ValueError(
            f"Uploaded file must include order id, order date, and revenue/sales amount columns. "
            f"Missing: {missing}. Found columns: {available}"
        )

    df = _fill_optional_columns(df)
    df = df.drop_duplicates(subset=["Order_ID", "Product_Name", "Order_Date"]).copy()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid_counts = df[NUMERIC_COLUMNS + ["Order_Date"]].isna().sum()
    invalid_counts = invalid_counts[invalid_counts > 0]
    if not invalid_counts.empty:
        details = ", ".join(f"{col}: {count}" for col, count in invalid_counts.items())
        raise ValueError(f"CSV has invalid values in {details}")

    df = df.sort_values("Order_Date").reset_index(drop=True)
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Num"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Year"] = df["Order_Date"].dt.year
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()
    df["Week_Num"] = df["Order_Date"].dt.isocalendar().week.astype(int)
    df["Profit_Margin"] = _safe_pct(df["Profit"], df["Revenue"])
    return df


def get_data_quality_summary(df):
    """Return source and quality stats displayed in the dashboard."""
    return {
        "rows": len(df),
        "orders": df["Order_ID"].nunique(),
        "customers": df["Customer_ID"].nunique(),
        "products": df["Product_Name"].nunique(),
        "cities": df["City"].nunique(),
        "start_date": df["Order_Date"].min(),
        "end_date": df["Order_Date"].max(),
        "missing_values": int(df.isna().sum().sum()),
    }


def get_kpi_metrics(df):
    """Compute headline KPI metrics."""
    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_quantity = df["Quantity"].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    unique_customers = df["Customer_ID"].nunique()
    avg_discount = df["Discount"].mean() * 100 if len(df) else 0

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
    monthly["Profit_Margin"] = _safe_pct(monthly["Profit"], monthly["Revenue"])
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
    cat_perf["Profit_Margin"] = _safe_pct(cat_perf["Profit"], cat_perf["Revenue"]).round(2)
    cat_perf["Revenue_Share"] = _safe_pct(cat_perf["Revenue"], cat_perf["Revenue"].sum()).round(2)
    return cat_perf.sort_values("Revenue", ascending=False)


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
    sub_perf["Profit_Margin"] = _safe_pct(sub_perf["Profit"], sub_perf["Revenue"]).round(2)
    return sub_perf.sort_values("Revenue", ascending=False)


def get_regional_analysis(df):
    """Region-wise performance."""
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
    regional["Profit_Margin"] = _safe_pct(regional["Profit"], regional["Revenue"]).round(2)
    regional["Revenue_Share"] = _safe_pct(regional["Revenue"], regional["Revenue"].sum()).round(2)
    return regional.sort_values("Revenue", ascending=False)


def get_city_analysis(df, top_n=15):
    """City-level performance."""
    city = (
        df.groupby(["City", "State", "Region"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(top_n)
    )
    city["Profit_Margin"] = _safe_pct(city["Profit"], city["Revenue"]).round(2)
    return city


def get_seasonal_analysis(df):
    """Quarterly performance."""
    quarterly = (
        df.groupby(["Year", "Quarter"])
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
        .sort_values(["Year", "Quarter"])
    )
    quarterly["Quarter_Label"] = "Q" + quarterly["Quarter"].astype(str) + " " + quarterly["Year"].astype(str)
    quarterly["Profit_Margin"] = _safe_pct(quarterly["Profit"], quarterly["Revenue"]).round(2)
    return quarterly


def get_customer_segments(df):
    """Segment-wise analysis."""
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
    segments["Profit_Margin"] = _safe_pct(segments["Profit"], segments["Revenue"]).round(2)
    segments["Revenue_Share"] = _safe_pct(segments["Revenue"], segments["Revenue"].sum()).round(2)
    return segments.sort_values("Revenue", ascending=False)


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
    payment["Revenue_Share"] = _safe_pct(payment["Revenue"], payment["Revenue"].sum()).round(2)
    return payment


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
    shipping["Revenue_Share"] = _safe_pct(shipping["Revenue"], shipping["Revenue"].sum()).round(2)
    return shipping


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
    )
    products["Profit_Margin"] = _safe_pct(products["Profit"], products["Revenue"]).round(2)
    return products.sort_values(metric, ascending=ascending).head(n)


def get_yoy_growth(df):
    """Year-over-year growth comparison."""
    yearly = (
        df.groupby("Year")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Customers=("Customer_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Year")
    )
    yearly["Revenue_Growth"] = yearly["Revenue"].pct_change() * 100
    yearly["Profit_Growth"] = yearly["Profit"].pct_change() * 100
    return yearly


def get_profit_margin_heatmap_data(df):
    """Profit margin by Category and Region for heatmap."""
    profit = df.pivot_table(values="Profit", index="Category", columns="Region", aggfunc="sum").fillna(0)
    revenue = df.pivot_table(values="Revenue", index="Category", columns="Region", aggfunc="sum").fillna(0)
    heatmap = (profit / revenue.replace(0, np.nan) * 100).fillna(0)
    return heatmap.round(2)


def get_3d_surface_data(df):
    """Revenue by Month and Category for 3D surface plot."""
    return df.pivot_table(values="Revenue", index="Month_Num", columns="Category", aggfunc="sum").fillna(0)


def get_3d_scatter_data(df):
    """Prepare data for 3D scatter: quantity, unit price, and profit."""
    return (
        df.groupby(["Product_Name", "Category", "Sub_Category"])
        .agg(
            Quantity=("Quantity", "sum"),
            Avg_Price=("Unit_Price", "mean"),
            Profit=("Profit", "sum"),
            Revenue=("Revenue", "sum"),
        )
        .reset_index()
    )


def get_3d_bar_data(df):
    """City by Category by Revenue for 3D city chart."""
    bar_data = df.pivot_table(values="Revenue", index="City", columns="Category", aggfunc="sum").fillna(0)
    bar_data["Total"] = bar_data.sum(axis=1)
    return bar_data.sort_values("Total", ascending=False).head(10).drop("Total", axis=1)


def get_discount_profit_correlation(df):
    """Discount vs profit correlation data."""
    return (
        df.groupby(["Category", "Discount"])
        .agg(
            Avg_Profit=("Profit", "mean"),
            Avg_Revenue=("Revenue", "mean"),
            Count=("Order_ID", "count"),
        )
        .reset_index()
    )


def generate_business_insights(df, kpis):
    """Generate key findings from the currently filtered data."""
    insights = []
    cat_perf = get_category_performance(df)
    if not cat_perf.empty:
        top_cat = cat_perf.iloc[0]
        insights.append({
            "icon": "trending_up",
            "title": "Top Revenue Category",
            "text": f"{top_cat['Category']} leads with {_format_money(top_cat['Revenue'])}, contributing {top_cat['Revenue_Share']:.1f}% of revenue.",
            "type": "success",
        })

        most_profitable = cat_perf.sort_values("Profit_Margin", ascending=False).iloc[0]
        insights.append({
            "icon": "account_balance_wallet",
            "title": "Highest Profit Margin",
            "text": f"{most_profitable['Category']} has the highest category margin at {most_profitable['Profit_Margin']:.1f}%.",
            "type": "info",
        })

    regional = get_regional_analysis(df)
    if not regional.empty:
        top_region = regional.iloc[0]
        insights.append({
            "icon": "location_on",
            "title": "Strongest Region",
            "text": f"{top_region['Region']} leads with {_format_money(top_region['Revenue'])} and {int(top_region['Orders'])} orders.",
            "type": "success",
        })

    monthly = get_monthly_trends(df)
    if not monthly.empty:
        peak_month = monthly.loc[monthly["Revenue"].idxmax()]
        insights.append({
            "icon": "calendar_month",
            "title": "Peak Sales Month",
            "text": f"{peak_month['Month_Label']} recorded the highest revenue at {_format_money(peak_month['Revenue'])}.",
            "type": "warning",
        })

    segments = get_customer_segments(df)
    if not segments.empty:
        top_segment = segments.iloc[0]
        insights.append({
            "icon": "groups",
            "title": "Dominant Customer Segment",
            "text": f"{top_segment['Segment']} customers account for {top_segment['Revenue_Share']:.1f}% of revenue across {int(top_segment['Customers'])} customers.",
            "type": "info",
        })

    high_disc = df[df["Discount"] >= 0.20]
    low_disc = df[df["Discount"] < 0.10]
    if len(high_disc) and len(low_disc):
        high_margin = high_disc["Profit_Margin"].mean()
        low_margin = low_disc["Profit_Margin"].mean()
        insight_type = "danger" if high_margin < low_margin else "success"
        insights.append({
            "icon": "sell",
            "title": "Discount Impact",
            "text": f"20%+ discount orders average {high_margin:.1f}% margin versus {low_margin:.1f}% for orders under 10% discount.",
            "type": insight_type,
        })

    yoy = get_yoy_growth(df)
    if len(yoy) > 1 and not pd.isna(yoy.iloc[-1]["Revenue_Growth"]):
        growth = yoy.iloc[-1]["Revenue_Growth"]
        direction = "grew" if growth > 0 else "declined"
        insights.append({
            "icon": "show_chart",
            "title": "Year-over-Year Growth",
            "text": f"Revenue {direction} by {abs(growth):.1f}% in {int(yoy.iloc[-1]['Year'])} versus {int(yoy.iloc[-2]['Year'])}.",
            "type": "success" if growth > 0 else "danger",
        })

    return insights


def get_strategic_recommendations(df):
    """Generate recommendation cards from the currently filtered data."""
    recommendations = []

    monthly = get_monthly_trends(df)
    if len(monthly) > 1:
        peak_month = monthly.loc[monthly["Revenue"].idxmax()]
        avg_monthly_revenue = monthly["Revenue"].mean()
        lift = ((peak_month["Revenue"] - avg_monthly_revenue) / avg_monthly_revenue * 100) if avg_monthly_revenue else 0
        recommendations.append({
            "icon": "calendar_month",
            "title": "Plan Around Peak Demand",
            "text": f"{peak_month['Month_Label']} is the strongest month at {_format_money(peak_month['Revenue'])}, {lift:.1f}% above the filtered monthly average.",
            "color": "#38BDF8",
        })

    high_disc = df[df["Discount"] >= 0.20]
    low_disc = df[df["Discount"] < 0.10]
    if len(high_disc) and len(low_disc):
        high_margin = high_disc["Profit_Margin"].mean()
        low_margin = low_disc["Profit_Margin"].mean()
        recommendations.append({
            "icon": "sell",
            "title": "Tighten Deep Discounting",
            "text": f"20%+ discount orders average {high_margin:.1f}% margin versus {low_margin:.1f}% for under-10% discount orders.",
            "color": "#F59E0B",
        })

    segments = get_customer_segments(df)
    if not segments.empty:
        best_segment = segments.sort_values("Avg_Order_Value", ascending=False).iloc[0]
        recommendations.append({
            "icon": "groups",
            "title": "Prioritize High-Value Customers",
            "text": f"{best_segment['Segment']} has the highest average order value at {_format_money(best_segment['Avg_Order_Value'])} across {int(best_segment['Customers'])} customers.",
            "color": "#22C55E",
        })

    cat_perf = get_category_performance(df)
    if not cat_perf.empty:
        high_margin_cat = cat_perf.sort_values("Profit_Margin", ascending=False).iloc[0]
        recommendations.append({
            "icon": "inventory_2",
            "title": "Push the Best-Margin Category",
            "text": f"{high_margin_cat['Category']} leads margin at {high_margin_cat['Profit_Margin']:.1f}% and contributes {high_margin_cat['Revenue_Share']:.1f}% of revenue.",
            "color": "#14B8A6",
        })

    regional = get_regional_analysis(df)
    if len(regional) > 1:
        weakest_region = regional.sort_values("Revenue").iloc[0]
        strongest_region = regional.sort_values("Revenue", ascending=False).iloc[0]
        gap = strongest_region["Revenue"] - weakest_region["Revenue"]
        recommendations.append({
            "icon": "location_on",
            "title": "Close the Regional Revenue Gap",
            "text": f"{weakest_region['Region']} trails {strongest_region['Region']} by {_format_money(gap)} in filtered revenue.",
            "color": "#EF4444",
        })

    payment = get_payment_analysis(df)
    if not payment.empty:
        top_payment = payment.iloc[0]
        recommendations.append({
            "icon": "payments",
            "title": "Lean Into Preferred Payment Mode",
            "text": f"{top_payment['Payment_Mode']} contributes {top_payment['Revenue_Share']:.1f}% of revenue across {int(top_payment['Orders'])} orders.",
            "color": "#A855F7",
        })

    return recommendations
