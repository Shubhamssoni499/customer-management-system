import streamlit as st
if not st.session_state.get("logged_in", False):
    st.warning("Please open the app via the main page and login first: `streamlit run app.py`")
    st.stop()
import pandas as pd
from services.customer_service import CustomerService

customer_service = CustomerService()

st.title("Customers")
st.write("Manage customers — add, search, edit, delete.")

# -- Add customer form (compact)
with st.form("add_customer", clear_on_submit=True):
    st.markdown("### ➕ Add Customer")
    c1, c2 = st.columns(2)
    name = c1.text_input("Name")
    email = c2.text_input("Email")
    phone = c1.text_input("Phone")
    address = c2.text_input("Address")
    submitted = st.form_submit_button("Add Customer")
    if submitted:
        if name and email:
            customer_service.add_customer(name, email, phone, address)
            st.success("Customer added ")
        else:
            st.warning("Name and Email required.")

st.markdown("---")

# -- Search & show table
q = st.text_input("Search by name / email", "")
customers = customer_service.get_all_customers() or []
df = pd.DataFrame(customers)

if q:
    df = df[df.apply(lambda r: q.lower() in str(r.values).lower(), axis=1)]

if not df.empty:
    st.dataframe(df.reset_index(drop=True))
    # quick delete/edit UI (simple)
    sel = st.number_input("Enter ID to delete (or 0 to skip)", min_value=0, value=0)
    if st.button("Delete by ID") and sel > 0:
        customer_service.delete_customer(int(sel))
        st.success("Deleted ✅")
        st.rerun()
else:
    st.info("No customers to show. Add new customers using the form above.")