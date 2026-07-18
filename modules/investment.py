import streamlit as st
import pandas as pd
import plotly.express as px

from services.investment_engine import simulate_investment


def show_investment():

    st.title("📈 Investment Simulator")

    initial = st.number_input(
        "Initial Investment (£)",
        min_value=0.0,
        value=10000.0,
    )

    monthly = st.number_input(
        "Monthly Investment (£)",
        min_value=0.0,
        value=300.0,
    )

    annual_return = st.slider(
        "Expected Annual Return (%)",
        min_value=1.0,
        max_value=15.0,
        value=8.0,
    )

    years = st.slider(
        "Investment Period (Years)",
        min_value=1,
        max_value=40,
        value=20,
    )

    if st.button("📊 Run Simulation"):

        results = simulate_investment(
            initial,
            monthly,
            annual_return,
            years,
        )

        df = pd.DataFrame(results)

        st.subheader("Investment Projection")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        fig = px.line(
            df,
            x="Year",
            y="Portfolio Value",
            markers=True,
            title="Portfolio Growth",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        final_value = df.iloc[-1]["Portfolio Value"]

        total_invested = initial + (monthly * 12 * years)

        profit = final_value - total_invested

        roi = (profit / total_invested) * 100 if total_invested else 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Invested",
                f"£{total_invested:,.2f}",
            )

        with col2:
            st.metric(
                "Portfolio Value",
                f"£{final_value:,.2f}",
            )

        with col3:
            st.metric(
                "Profit",
                f"£{profit:,.2f}",
            )

        with col4:
            st.metric(
                "ROI",
                f"{roi:.2f}%",
            )

        st.download_button(
            "⬇ Download Results",
            df.to_csv(index=False),
            file_name="investment_projection.csv",
            mime="text/csv",
        )