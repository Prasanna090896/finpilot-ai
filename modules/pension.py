import streamlit as st
import pandas as pd
import plotly.express as px

from services.pension_engine import calculate_pension_projection


def show_pension():

    st.title("💰 Pension Planner")

    current_age = st.number_input(
        "Current Age",
        min_value=18,
        max_value=100,
        value=30,
    )

    retirement_age = st.number_input(
        "Retirement Age",
        min_value=50,
        max_value=75,
        value=65,
    )

    current_pension = st.number_input(
        "Current Pension (£)",
        min_value=0.0,
        value=10000.0,
    )

    monthly = st.number_input(
        "Monthly Contribution (£)",
        min_value=0.0,
        value=300.0,
    )

    annual_return = st.slider(
        "Expected Annual Return (%)",
        1.0,
        12.0,
        7.0,
    )

    if st.button("📈 Calculate Projection"):

        results = calculate_pension_projection(
            current_age,
            retirement_age,
            current_pension,
            monthly,
            annual_return,
        )

        df = pd.DataFrame(results)

        st.subheader("Projection")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        fig = px.line(
            df,
            x="Age",
            y="Projected Pension",
            markers=True,
            title="Projected Pension Growth",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        final_value = df.iloc[-1]["Projected Pension"]

        years = retirement_age - current_age

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Years Remaining",
                years,
            )

        with col2:
            st.metric(
                "Retirement Value",
                f"£{final_value:,.2f}",
            )

        with col3:
            gain = final_value - current_pension
            st.metric(
                "Estimated Growth",
                f"£{gain:,.2f}",
            )

        st.download_button(
            "⬇ Download Projection",
            df.to_csv(index=False),
            "pension_projection.csv",
            "text/csv",
        )