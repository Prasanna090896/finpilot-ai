import streamlit as st

from services.report_generator import generate_report

def show_reports():

    st.title("📄 Financial Report Generator")

    st.write(
        "Generate a personalised financial planning report."
    )

    name = st.text_input("Customer Name")

    age = st.number_input(
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

    pension = st.number_input(
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
        min_value=1.0,
        max_value=12.0,
        value=7.0,
    )
    if st.button("📄 Generate Report"):

        report = generate_report(
            name,
            age,
            retirement_age,
            pension,
            monthly,
            annual_return,
        )

        st.success("Report Generated Successfully")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Current Age", age)

        with col2:
            st.metric("Retirement Age", retirement_age)

        with col3:
            st.metric(
                "Years Remaining",
                retirement_age - age,
            )

        st.divider()

        st.subheader("Financial Report")

        st.text_area(
            "Report",
            report,
            height=300,
        )
        report_text = f"""
FINPILOT AI FINANCIAL REPORT

====================================

Customer Name : {name}

Current Age : {age}

Retirement Age : {retirement_age}

Current Pension : £{pension:,.2f}

Monthly Contribution : £{monthly:,.2f}

Expected Return : {annual_return}%

====================================

REPORT

{report}

====================================

AI recommendations are available from the AI Advisor page.
"""

        st.download_button(
            label="⬇ Download Report (.txt)",
            data=report_text,
            file_name=f"{name}_financial_report.txt",
            mime="text/plain",
        )

        st.info(
            "Use the AI Advisor page for personalised GPT-powered recommendations."
        )