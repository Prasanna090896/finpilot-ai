import streamlit as st

from modules.dashboard import show_dashboard
from modules.customers import show_customers
from modules.pension import show_pension
from modules.investment import show_investment
from modules.advisor import show_advisor
from modules.reports import show_reports


st.set_page_config(
    page_title="FinPilot AI",
    page_icon="🤖",
    layout="wide",
)

st.sidebar.title("🤖 FinPilot AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customers",
        "Pension Planner",
        "Investment Simulator",
        "AI Advisor",
        "Reports",
    ],
)

if page == "Dashboard":
    show_dashboard()

elif page == "Customers":
    show_customers()

elif page == "Pension Planner":
    show_pension()

elif page == "Investment Simulator":
    show_investment()

elif page == "AI Advisor":
    show_advisor()

elif page == "Reports":
    show_reports()