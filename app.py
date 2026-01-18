import streamlit as st
from services.auth_service import AuthService

# -------------------------
# Streamlit basic config
# -------------------------
st.set_page_config(page_title="Customer Management System", page_icon="📦", layout="wide")

auth = AuthService()

# -------------------------
# Session init
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

# -------------------------
# LOGIN PAGE
# -------------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.login(username, password)
        except Exception as e:
            st.error("Database connection failed. Check console.")
            print("Login error:", e)
            return

        if user:
            # store minimal trusted info in session
            st.session_state["logged_in"] = True
            # store only safe fields from user (avoid storing DB objects)
            st.session_state["user"] = {
                "id": user.get("id"),
                "username": user.get("username"),
                "role": user.get("role")
            }
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()  # do not render rest of app until login

# -------------------------
# MAIN (after login)
# -------------------------
def main_page():
    st.sidebar.title("📌 Menu")

    user = st.session_state.get("user") or {}
    role = user.get("role", "staff")

    # role based menu
    if role == "admin":
        menu_options = ["Dashboard", "Customers", "Inquiries", "Users", "Logout"]
    else:
        menu_options = ["Dashboard", "Customers", "Inquiries", "Logout"]

    menu = st.sidebar.selectbox("Navigate", menu_options)

    st.sidebar.write("---")
    st.sidebar.write(f"👤 Logged in as: **{user.get('username','-')}**")
    st.sidebar.write(f"🔖 Role: **{role}**")

    # routing — import inside block to avoid import-time DB calls
    if menu == "Dashboard":
        from pages import dashboard  # pages/dashboard.py must be page-style file (no function)
        # dashboard module executes on import (Streamlit page model)
    elif menu == "Customers":
        from pages.customers import customers_page
        customers_page()
    elif menu == "Inquiries":
        from pages.inquiries import inquiries_page
        inquiries_page()
    elif menu == "Users":
        # double-safe: only allow admin
        if role != "admin":
            st.warning("Access denied — admin only")
        else:
            from pages.users import users_page
            users_page()
    elif menu == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()

# -------------------------
# START
# -------------------------
if st.session_state["logged_in"]:
    main_page()
else:
    login_page()