import streamlit as st
if not st.session_state.get("logged_in", False):
    st.warning("Please open the app via the main page and login first: `streamlit run app.py`")
    st.stop()
import pandas as pd
from services.inquiry_service import InquiryService
from services.customer_service import CustomerService

inq = InquiryService()
cust = CustomerService()

st.title("📩 Inquiries")
st.write("Manage customer inquiries — add, view, update, delete.")

# --------------------
# ADD NEW INQUIRY
# --------------------
with st.form("add_inquiry", clear_on_submit=True):
    st.subheader("➕ Add New Inquiry")

    customers = cust.get_all_customers() or []
    customer_map = {c["id"]: c["name"] for c in customers}

    customer_id = st.selectbox("Select Customer", options=list(customer_map.keys()))
    inquiry_text = st.text_area("Enter Inquiry")

    submitted = st.form_submit_button("Submit")
    if submitted:
        inq.add_inquiry(customer_id, inquiry_text)
        st.success("Inquiry added successfully!")
        st.rerun()

st.markdown("---")

# --------------------
# SHOW ALL INQUIRIES
# --------------------
inquiries = inq.get_all_inquiries() or []

if not inquiries:
    st.info("No inquiries found.")
    st.stop()

df = pd.DataFrame(inquiries)

st.subheader("📜 All Inquiries")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# --------------------------
# UPDATE INQUIRY STATUS
# --------------------------
st.subheader("🔄 Update Inquiry Status")

selected_id = st.number_input("Select Inquiry ID", min_value=1)

new_status = st.selectbox("New Status", ["Pending", "Resolved"])

if st.button("Update Status"):
    inq.update_inquiry(selected_id, new_status)
    st.success("Status updated successfully!")
    st.rerun()

st.markdown("---")

# --------------------------
# DELETE INQUIRY
# --------------------------
st.subheader("🗑 Delete Inquiry")

delete_id = st.number_input("Inquiry ID to delete", min_value=1, key="delete")
if st.button("Delete Inquiry"):
    inq.delete_inquiry(delete_id)
    st.success("Inquiry deleted!")
    st.rerun()