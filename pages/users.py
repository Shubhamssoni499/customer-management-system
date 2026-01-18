import streamlit as st
import pandas as pd
from services.user_service import UserService


# --------------------------------
# LOGIN CHECK (security guard)
# --------------------------------
def guard():
    if not st.session_state.get("logged_in", False):
        st.warning("Please login first!")
        st.stop()


# --------------------------------
# USERS PAGE FUNCTION (this was missing!)
# --------------------------------
def users_page():
    guard()   # apply login guard

    svc = UserService()

    st.title("👥 Users Management")
    st.write("Create admin/staff users and view the list.")

    # ---------- Add User Form ----------
    with st.form("add_user", clear_on_submit=True):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "staff"])
        btn = st.form_submit_button("Create User")

        if btn:
            if uname and pwd:
                svc.add_user(uname, pwd, role)
                st.success("User created successfully!")
                st.rerun()
            else:
                st.warning("Please fill all fields.")

    st.markdown("---")

    # ---------- User Table ----------
    users = svc.get_all_users() or []
    if users:
        st.dataframe(pd.DataFrame(users))
    else:
        st.info("No users found.")