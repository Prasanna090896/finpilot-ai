import streamlit as st

from database import SessionLocal
from services.auth_service import authenticate


def login():

    st.title("🔐 FinPilot AI Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        db = SessionLocal()

        user = authenticate(
            db,
            username,
            password
        )

        db.close()

        if user:

            st.session_state.logged_in = True
            st.session_state.user = user.full_name

            st.rerun()

        else:
            st.error("Invalid username or password.")