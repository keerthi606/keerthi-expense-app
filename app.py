import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("✨ KEERTHI MONTHLY EXPENSES TRACKER ✨")

# 2. Google Sheets Connection
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_info(
        dict(st.secrets["connections"]["gsheets"]),
        scopes=scope
    )
    client = gspread.authorize(creds)
    
    # Direct ga first worksheet/tab ni open chesthundi
    sheet = client.open_by_key("1P_EY8UX8Iviz3TLv8Ige1SDXEJCn0TkRsX_gSqz0v4").sheet1
except Exception as e:
    st.error(f"Google Sheets కనెక్షన్ ఎర్రర్: {e}")
    st.stop()

# 3. Load Existing Data
try:
    records = sheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
    else:
        df = pd.DataFrame(columns=["S NO", "Date", "Month", "House", "Transaction Type", "Category", "Description", "Amount", "Payment Mode"])
except Exception as e:
    df = pd.DataFrame(columns=["S NO", "Date", "Month", "House", "Transaction Type", "Category", "Description", "Amount", "Payment Mode"])

# 4. Form for New Entry
st.subheader("➕ Add New Expense / Income")

with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date = st.date_input("Date")
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        house = st.selectbox("House", ["Home", "Office", "Other"])
        
    with col2:
        trans_type = st.selectbox("Transaction Type", ["Expense", "Income"])
        category = st.text_input("Category (e.g. Groceries, Rent, Fuel)")
        description = st.text_input("Description")
        
    with col3:
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        payment_mode = st.selectbox("Payment Mode", ["UPI", "Cash", "Credit Card", "Bank Transfer"])
        
    submitted = st.form_submit_button("Save Entry")

if submitted:
    s_no = len(df) + 1
    new_row = [s_no, str(date), month, house, trans_type, category, description, amount, payment_mode]
    
    try:
        sheet.append_row(new_row)
        st.success("✅ Entry successfully saved to Google Sheet!")
        st.rerun()
    except Exception as e:
        st.error(f"డేటా సేవ్‌ చేయడంలో ఎర్రర్ వచ్చింది: {e}")

# 5. Display Data Table
st.subheader("📊 Expense Records")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("ఇంకా ఏ డేటా లేదు. పైన ఉన్న ఫారమ్ ఉపయోగించి ఎంట్రీలు యాడ్ చేయండి.")
