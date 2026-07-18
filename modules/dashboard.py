import streamlit as st
import pandas as pd
import plotly.express as px

from database import SessionLocal
from services.customer_service import get_customers


def show_dashboard():

    st.title("📊 FinPilot AI Dashboard")

    db = SessionLocal()

    customers = get_customers(db)

    if not customers:
        st.info("No customer data available.")
        db.close()
        return

    df = pd.DataFrame(
        [
            {
                "Name": c.name,
                "Age": c.age,
                "Retirement Age": c.retirement_age,
                "Pension": c.pension,
                "Monthly": c.monthly_contribution,
                "Return": c.annual_return,
            }
            for c in customers
        ]
    )
    # ======================================
    # Sidebar Filters
    # ======================================

    st.sidebar.header("Dashboard Filters")

    search = st.sidebar.text_input(
        "🔍 Search Customer"
    )

    min_pension = st.sidebar.number_input(
        "Minimum Pension (£)",
        min_value=0,
        value=0,
    )

    max_pension = st.sidebar.number_input(
        "Maximum Pension (£)",
        min_value=0,
        value=int(df["Pension"].max()),
    )

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(
                search,
                case=False,
            )
        ]

    filtered_df = filtered_df[
        (filtered_df["Pension"] >= min_pension)
        &
        (filtered_df["Pension"] <= max_pension)
    ]

    if filtered_df.empty:
        st.warning("No customers match the selected filters.")
        db.close()
        return

    # ======================================
    # KPI Cards
    # ======================================

    total_customers = len(filtered_df)
    total_assets = filtered_df["Pension"].sum()
    average_pension = filtered_df["Pension"].mean()
    total_monthly = filtered_df["Monthly"].sum()
    average_return = filtered_df["Return"].mean()
    average_retirement = filtered_df["Retirement Age"].mean()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "👥 Customers",
            total_customers,
        )

    with c2:
        st.metric(
            "💷 Total Assets",
            f"£{total_assets:,.0f}",
        )

    with c3:
        st.metric(
            "🏦 Average Pension",
            f"£{average_pension:,.0f}",
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "💰 Monthly Contributions",
            f"£{total_monthly:,.0f}",
        )

    with c5:
        st.metric(
            "📈 Average Return",
            f"{average_return:.1f}%",
        )

    with c6:
        st.metric(
            "🎯 Avg Retirement Age",
            f"{average_retirement:.1f}",
        )

    st.divider()
    # ======================================
    # Dashboard Charts
    # ======================================

    st.subheader("📊 Dashboard Analytics")

    col1, col2 = st.columns(2)

    with col1:

        fig_pension = px.histogram(
            filtered_df,
            x="Pension",
            nbins=10,
            title="Pension Distribution",
        )

        st.plotly_chart(
            fig_pension,
            width="stretch",
            key="pension_distribution",
        )

    with col2:

        fig_age = px.histogram(
            filtered_df,
            x="Age",
            nbins=10,
            title="Customer Age Distribution",
        )

        st.plotly_chart(
            fig_age,
            width="stretch",
            key="age_distribution",
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        top10 = filtered_df.sort_values(
            "Pension",
            ascending=False,
        ).head(10)

        fig_top10 = px.bar(
            top10,
            x="Name",
            y="Pension",
            title="Top 10 Customers by Pension",
            text_auto=True,
        )

        st.plotly_chart(
            fig_top10,
            width="stretch",
            key="top10_customers",
        )

    with col4:

        fig_monthly = px.bar(
            filtered_df,
            x="Name",
            y="Monthly",
            title="Monthly Contributions",
            text_auto=True,
        )

        st.plotly_chart(
            fig_monthly,
            width="stretch",
            key="monthly_contributions",
        )

    st.divider()

    col5, col6 = st.columns(2)

    with col5:

        retirement_chart = (
            filtered_df
            .groupby("Retirement Age")
            .size()
            .reset_index(name="Customers")
        )

        fig_retirement = px.bar(
            retirement_chart,
            x="Retirement Age",
            y="Customers",
            title="Retirement Age Distribution",
            text_auto=True,
        )

        st.plotly_chart(
            fig_retirement,
            width="stretch",
            key="retirement_distribution",
        )

    with col6:

        fig_assets = px.pie(
            filtered_df,
            names="Name",
            values="Pension",
            title="Assets by Customer",
        )

        st.plotly_chart(
            fig_assets,
            width="stretch",
            key="assets_distribution",
        )

    st.divider()

    st.subheader("📋 Recent Customers")

    recent = filtered_df.tail(5).copy()

    for col in recent.columns:
        if recent[col].dtype == "object":
            recent[col] = recent[col].astype(str)

    st.dataframe(
        recent,
        width="stretch",
        hide_index=True,
    )

    st.divider()
    # ======================================
    # Executive Insights
    # ======================================

    st.subheader("📈 Executive Insights")

    highest_customer = filtered_df.loc[
        filtered_df["Pension"].idxmax()
    ]

    lowest_customer = filtered_df.loc[
        filtered_df["Pension"].idxmin()
    ]

    avg_monthly = filtered_df["Monthly"].mean()

    common_retirement = (
        filtered_df["Retirement Age"]
        .mode()
        .iloc[0]
    )

    left, right = st.columns(2)

    with left:

        st.success(
            f"""
### 🏆 Highest Pension Holder

**{highest_customer['Name']}**

Current Pension: **£{highest_customer['Pension']:,.0f}**
"""
        )

        st.info(
            f"""
### 💰 Average Monthly Contribution

**£{avg_monthly:,.0f}**
"""
        )

    with right:

        st.warning(
            f"""
### 📉 Lowest Pension Holder

**{lowest_customer['Name']}**

Current Pension: **£{lowest_customer['Pension']:,.0f}**
"""
        )

        st.info(
            f"""
### 🎯 Most Common Retirement Age

**{common_retirement} years**
"""
        )

    st.divider()

    # ======================================
    # Portfolio Summary
    # ======================================

    st.subheader("📋 Portfolio Summary")

    summary = pd.DataFrame(
        {
            "Metric": [
                "Customers",
                "Total Assets",
                "Average Pension",
                "Monthly Contributions",
                "Average Return",
                "Average Retirement Age",
            ],
            "Value": [
                str(total_customers),
                f"£{total_assets:,.0f}",
                f"£{average_pension:,.0f}",
                f"£{total_monthly:,.0f}",
                f"{average_return:.1f}%",
                f"{average_retirement:.1f} years",
            ],
        }
    )

    summary = summary.astype(str)

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    st.caption(
        "© 2026 FinPilot AI | Financial Planning & Wealth Management Dashboard"
    )

    db.close()