import streamlit as st
import pandas as pd
from io import BytesIO

from database import SessionLocal
from services.customer_service import (
    add_customer,
    get_customer,
    get_customers,
    update_customer,
    delete_customer,
)


def show_customers():

    st.title("👤 Customer Management")

    db = SessionLocal()

    customers = get_customers(db)

    # ============================
    # Dashboard Metrics
    # ============================

    total_customers = len(customers)

    total_assets = sum(c.pension for c in customers)

    average_age = (
        sum(c.age for c in customers) / total_customers
        if total_customers else 0
    )

    average_pension = (
        total_assets / total_customers
        if total_customers else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Customers", total_customers)

    with col2:
        st.metric(
            "💷 Assets",
            f"£{total_assets:,.0f}"
        )

    with col3:
        st.metric(
            "🎂 Avg Age",
            f"{average_age:.1f}"
        )

    with col4:
        st.metric(
            "🏦 Avg Pension",
            f"£{average_pension:,.0f}"
        )

    st.divider()

    # ============================
    # Tabs
    # ============================

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Customer",
            "✏ Edit Customer",
            "📋 Customer List",
        ]
    )

    # ============================
    # TAB 1 - ADD CUSTOMER
    # ============================

    with tab1:

        st.subheader("Add New Customer")

        with st.form("customer_form"):

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
                1.0,
                12.0,
                7.0,
            )

            submitted = st.form_submit_button(
                "💾 Save Customer"
            )

        if submitted:

            if not name.strip():

                st.error("Customer name is required.")

            elif retirement_age <= age:

                st.error(
                    "Retirement age must be greater than current age."
                )

            else:

                add_customer(
                    db,
                    name,
                    age,
                    retirement_age,
                    pension,
                    monthly,
                    annual_return,
                )

                st.success(
                    "✅ Customer saved successfully."
                )

                st.rerun()

    # ============================
    # TAB 2 - CUSTOMER LIST
    # ============================

    with tab3:

        st.subheader("Customer List")

        search = st.text_input(
            "🔍 Search Customers",
            placeholder="Search by name, age or retirement age...",
        ).strip().lower()

        data = []

        for customer in customers:

            if search:

                if (
                    search not in customer.name.lower()
                    and search not in str(customer.age)
                    and search not in str(customer.retirement_age)
                ):
                    continue

            data.append(
                {
                    "ID": customer.id,
                    "Name": customer.name,
                    "Age": customer.age,
                    "Retirement Age": customer.retirement_age,
                    "Pension (£)": customer.pension,
                    "Monthly (£)": customer.monthly_contribution,
                    "Return (%)": customer.annual_return,
                }
            )

        if data:

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                width="stretch",
                height=400,
            )

            st.divider()

            # ============================
            # Export Buttons
            # ============================

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(
                    "⬇ Export CSV",
                    df.to_csv(index=False),
                    file_name="customers.csv",
                    mime="text/csv",
                )

            with col2:

                buffer = BytesIO()

                with pd.ExcelWriter(
                    buffer,
                    engine="openpyxl",
                ) as writer:

                    df.to_excel(
                        writer,
                        index=False,
                    )

                st.download_button(
                    "⬇ Export Excel",
                    buffer.getvalue(),
                    file_name="customers.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            st.divider()

            # ============================
            # Statistics
            # ============================

            st.subheader("📊 Customer Statistics")

            chart = (
                df.groupby("Retirement Age")
                .size()
            )

            st.bar_chart(chart)

        else:

            st.info("No matching customers found.")

    # ============================
    # TAB 2 - EDIT CUSTOMER
    # ============================

    with tab2:

        st.subheader("✏ Edit Customer")

        if customers:

            customer_options = {
                f"{customer.name} (ID: {customer.id})": customer.id
                for customer in customers
            }

            selected_name = st.selectbox(
                "Select Customer",
                list(customer_options.keys()),
            )

            selected_id = customer_options[selected_name]

            selected_customer = get_customer(
                db,
                selected_id,
            )

            with st.form("edit_customer_form"):

                edit_name = st.text_input(
                    "Customer Name",
                    value=selected_customer.name,
                )

                edit_age = st.number_input(
                    "Current Age",
                    min_value=18,
                    max_value=100,
                    value=selected_customer.age,
                )

                edit_retirement = st.number_input(
                    "Retirement Age",
                    min_value=50,
                    max_value=75,
                    value=selected_customer.retirement_age,
                )

                edit_pension = st.number_input(
                    "Current Pension (£)",
                    min_value=0.0,
                    value=float(selected_customer.pension),
                )

                edit_monthly = st.number_input(
                    "Monthly Contribution (£)",
                    min_value=0.0,
                    value=float(selected_customer.monthly_contribution),
                )

                edit_return = st.slider(
                    "Expected Annual Return (%)",
                    min_value=1.0,
                    max_value=12.0,
                    value=float(selected_customer.annual_return),
                )

                update = st.form_submit_button(
                    "💾 Update Customer"
                )

            if update:

                if edit_retirement <= edit_age:

                    st.error(
                        "Retirement age must be greater than current age."
                    )

                else:

                    update_customer(
                        db,
                        selected_id,
                        edit_name,
                        edit_age,
                        edit_retirement,
                        edit_pension,
                        edit_monthly,
                        edit_return,
                    )

                    st.success(
                        "✅ Customer updated successfully."
                    )

                    st.rerun()

        else:

            st.info("No customers available.")

    # ============================
    # DELETE CUSTOMER
    # ============================

    with tab3:

        st.divider()

        st.subheader("🗑 Delete Customer")

        if customers:

            delete_options = {
                f"{customer.name} (ID: {customer.id})": customer.id
                for customer in customers
            }

            delete_name = st.selectbox(
                "Select Customer to Delete",
                list(delete_options.keys()),
                key="delete_customer",
            )

            delete_id = delete_options[delete_name]

            confirm = st.checkbox(
                "I understand this action cannot be undone."
            )

            if confirm:

                if st.button(
                    "🗑 Delete Customer",
                    type="primary",
                ):

                    delete_customer(
                        db,
                        delete_id,
                    )

                    st.success(
                        "Customer deleted successfully."
                    )

                    st.rerun()

        else:

            st.info("No customers available.")

    db.close()