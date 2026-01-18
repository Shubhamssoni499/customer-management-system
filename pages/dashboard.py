import streamlit as st
if not st.session_state.get("logged_in", False):
    st.warning("Please open the app via the main page and login first: `streamlit run app.py`")
    st.stop()
import pandas as pd
from services.customer_service import CustomerService
from services.inquiry_service import InquiryService

st.title("📊 Dashboard")
st.write("Quick overview")

cust_svc = CustomerService()
inq_svc = InquiryService()

# ---- Fetch Data Safely ----
try:
    customers = cust_svc.get_all_customers() or []
    inquiries = inq_svc.get_all_inquiries() or []
except Exception as e:
    st.error("Database error. Check terminal logs.")
    print("Dashboard error:", e)
    st.stop()

total_customers = len(customers)
total_inquiries = len(inquiries)

# ---- Metrics ----
st.markdown("### 📌 Key Stats")
c1, c2 = st.columns(2)
c1.metric("Total Customers", total_customers)
c2.metric("Total Inquiries", total_inquiries)

st.markdown("---")

# ---- Chart ----
st.subheader("📈 Inquiries by Status")

if total_inquiries > 0:
    df = pd.DataFrame(inquiries)
    if "status" in df.columns:
        status_counts = df["status"].fillna("Unknown").value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("Status column not found.")
else:
    st.info("No inquiries yet.")

st.markdown("---")

# ---- Recent inquiries ----
st.subheader("🕒 Recent Inquiries")

if total_inquiries > 0:
    df_recent = pd.DataFrame(inquiries).head(5)
    st.dataframe(df_recent.reset_index(drop=True))
else:
    st.info("No recent inquiries to show.")