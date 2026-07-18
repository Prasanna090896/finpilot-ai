import streamlit as st

from database import SessionLocal
from services.customer_service import (
    get_customer,
    get_customers,
)
from services.ai_service import get_ai_advice


def show_advisor():

    st.title("🤖 AI Financial Advisor")

    db = SessionLocal()

    customers = get_customers(db)

    if not customers:
        st.warning("No customers found.")
        db.close()
        return

    customer_options = {
        f"{c.name} (ID: {c.id})": c.id
        for c in customers
    }

    selected = st.selectbox(
        "Select Customer",
        list(customer_options.keys()),
    )

    customer = get_customer(
        db,
        customer_options[selected],
    )

    st.divider()

    st.subheader("Customer Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Age", customer.age)
        st.metric("Current Pension", f"£{customer.pension:,.0f}")
        st.metric(
            "Monthly Contribution",
            f"£{customer.monthly_contribution:,.0f}",
        )

    with col2:
        st.metric("Retirement Age", customer.retirement_age)
        st.metric(
            "Expected Return",
            f"{customer.annual_return:.1f}%",
        )
        st.metric(
            "Years Until Retirement",
            customer.retirement_age - customer.age,
        )

    st.divider()

    question = st.text_area(
        "Ask AI",
        placeholder="Example: Can I retire comfortably at age 60?",
        height=120,
    )

    if st.button("🚀 Generate Advice"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating advice..."):

                try:

                    answer = get_ai_advice(
                        customer,
                        question,
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(f"Error: {e}")

    db.close()