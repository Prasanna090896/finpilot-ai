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

    selected_customer = st.selectbox(
        "Select Customer",
        list(customer_options.keys()),
    )

    customer = get_customer(
        db,
        customer_options[selected_customer],
    )

    st.divider()

    st.subheader("Customer Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Age",
            customer.age,
        )

        st.metric(
            "Current Pension",
            f"£{customer.pension:,.0f}",
        )

        st.metric(
            "Monthly Contribution",
            f"£{customer.monthly_contribution:,.0f}",
        )

    with col2:

        st.metric(
            "Retirement Age",
            customer.retirement_age,
        )

        st.metric(
            "Expected Return",
            f"{customer.annual_return:.1f}%",
        )

        years_left = (
            customer.retirement_age
            - customer.age
        )

        st.metric(
            "Years Until Retirement",
            years_left,
        )

    st.divider()

    st.subheader("Ask AI")

    question = st.text_area(
        "Ask a financial planning question",
        placeholder="Example: Can I retire comfortably at age 60?",
        height=120,
    )

    if st.button(
        "🚀 Generate Advice",
        use_container_width=True,
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Thinking..."
            ):

                try:

                    answer = get_ai_advice(
                        customer,
                        question,
                    )

                    st.success("AI Response")

                    st.markdown(answer)

                except Exception as e:

                    st.error(str(e))

    db.close()