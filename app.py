from io import BytesIO
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# Custom UI Styling
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        height: 50px;
        border: none;
        box-shadow: 0 4px 10px rgba(255, 65, 108, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #e0355d 0%, #e03f22 100%);
        color: white;
    }
    .welcome-text {
        text-align: center;
        color: #4A154B;
        font-size: 32px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .title-container {
        background: linear-gradient(90deg, #654ea3 0%, #eaafc8 100%);
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }
    .title-text {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: 1.5px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    h2, h3 {
        color: #1f3c88;
        font-weight: 700;
    }
    .footer-text {
        text-align: center;
        color: #4A154B;
        font-size: 30px;
        font-weight: 800;
        margin-top: 50px;
        padding: 20px;
        border-top: 3px dashed #654ea3;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Swagatham Heading
st.markdown(
    '<div class="welcome-text">🙏 Swagatham (స్వాగతం) 🙏</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="title-container">
        <p class="title-text">🌟 KEERTHI MONTHLY EXPENSES TRACKER 🌟</p>
    </div>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "expenses_data.csv"

# Data load cheyyadam mariyu dates/months set cheyyadam
try:
    df = pd.read_csv(DATA_FILE)
    if not df.empty and "Date" in df.columns:
        parsed_dates = pd.to_datetime(
            df["Date"], format="mixed", dayfirst=True, errors="coerce"
        )
        df["Date"] = parsed_dates.dt.strftime("%d-%m-%Y")
        df["Month"] = parsed_dates.dt.strftime("%B %Y")
        df = df.dropna(subset=["Date"])
except FileNotFoundError:
    df = pd.DataFrame(
        columns=[
            "S NO",
            "Date",
            "Month",
            "Transaction Type",
            "Category",
            "Description",
            "Amount",
            "Payment Mode",
        ]
    )

# Save success message chupinchadam
if "show_success" in st.session_state and st.session_state["show_success"]:
    st.success("✅ Save Successfully! Transaction vijayavantamga save aindi.")
    st.toast("🎉 Transaction save aindi!")
    st.session_state["show_success"] = False

# Metrics lekkinchadam (Month-wise mariyu Overall)
if not df.empty:
    available_months = sorted(df["Month"].unique().tolist(), reverse=True)
    selected_month_filter = st.selectbox(
        "Nivedika kosam nelani ennukondi (Select Month)", available_months
    )

    month_filtered_df = df[df["Month"] == selected_month_filter]

    # Selected month income & expenses
    m_income = month_filtered_df[month_filtered_df["Transaction Type"] == "INCOME"]["Amount"].sum()
    m_total_expense = month_filtered_df[month_filtered_df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
    
    # Credit Card expenses in selected month
    m_cc_expenses = month_filtered_df[
        (month_filtered_df["Transaction Type"] == "EXPENSE")
        & (month_filtered_df["Payment Mode"] == "CREDIT CARD")
    ]["Amount"].sum()
    
    # Bank/Cash expenses in selected month
    m_bank_expenses = m_total_expense - m_cc_expenses
    
    # Bank balance based on selected month income & non-cc expenses
    m_bank_balance = m_income - m_bank_expenses

    # Top metrics display matching Image 1 layout style but for selected month / overall
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("💰 Motham Adayam (Income)", f"₹ {m_income:,.2f}")
    mcol2.metric(
        "💸 Motham Kharchu (Expense)", 
        f"₹ {m_total_expense:,.2f}",
        delta=f"Bank: ₹{m_bank_expenses:,.2f} | CC: ₹{m_cc_expenses:,.2f}",
        delta_color="off"
    )
    mcol3.metric("🏦 Bank Balance", f"₹ {m_bank_balance:,.2f}")
    mcol4.metric("💳 Credit Card Kharchu", f"₹ {m_cc_expenses:,.2f}")
    st.markdown("---")

st.subheader("📝 Kothha Transaction Jodinchandi")

col1, col2 = st.columns(2)

with col1:
    next_sno = (
        int(df["S NO"].max()) + 1
        if (not df.empty and "S NO" in df.columns and not df["S NO"].isnull().all())
        else 1
    )
    st.number_input(
        "S NO * (Automatic)", value=next_sno, disabled=True, key="auto_sno"
    )

    date = st.date_input("Date *")
    formatted_date_preview = date.strftime("%d-%m-%Y")
    st.caption(f"📅 Enchukunna thedi roopam: **{formatted_date_preview}**")

    trans_type = st.radio(
        "Transaction Type *", ["INCOME", "EXPENSE"], horizontal=True
    )

    if trans_type == "INCOME":
        categories = [
            "Enchukondi...",
            "Opening Balance",
            "Jeetham / Vethanam",
            "Credit Card",
            "Loan",
            "Appu",
            "Ithara Adayam",
        ]
    else:
        categories = [
            "Enchukondi...",
            "Saruku",
            "Kooragayalu / Pandlu",
            "Paalu",
            "Perugu",
            "Petrol",
            "Credit Card Payment",
            "Vehicle Maintenance",
            "Appu",
            "DWACRA Loan",
            "Inti Runam (Home Loan)",
            "Dvisakra Vahana Runam (Bike Loan)",
            "Current Bill",
            "Paper Bill",
            "Tiffins / Hotel",
            "Movies / Vinodham",
            "Clothes",
            "Toys",
            "Mandulu / Medical",
            "Mobile Recharge / Dish / Internet",
            "School / College Fees",
            "Inti Addae (House Rent)",
            "Cylinder / Gas Bill",
            "Water Bill / Cans",
            "Pooja Samagri",
            "Prayana Kharchulu (Travel Expenses)",
            "Babu Pocket Money",
            "Papa Pocket Money",
            "Nanna Pocket Money",
            "Amma Pocket Money",
            "Marammatulu (Repairs & Maintenance)",
            "Viralalu (Donations / Charity)",
            "Seethala Paneeyalu (Cool Drinks)",
            "Chicken / Mutton / Fish",
            "Eggs",
            "Insurance / LIC",
            "Dry Fruits & Nuts",
            "Subhakaryalu / Bahumatulu (Gifts & Functions)",
            "Itharalu",
        ]

    category = st.selectbox("Category *", categories, key=f"cat_{trans_type}")

with col2:
    amount = st.number_input(
        "AMOUNT (₹) *", min_value=0.0, step=1.0, format="%.2f"
    )

    payment_modes = [
        "Enchukondi...",
        "GOOGLE PAY",
        "PHONE PE",
        "CASH",
        "CREDIT CARD",
        "BANK ACCOUNT",
        "OTHERS",
    ]
    payment_mode = st.selectbox("Payment Mode *", payment_modes)

    description = st.text_input(
        "Description (Evariki/Dheniki chellincharu?) *",
        placeholder="Udaharana: Ramayya gariki kirana samanlaki",
    )

st.markdown("")

if st.button("💾 SAVE TRANSACTION"):
    validation_passed = True
    error_message = ""

    if amount <= 0:
        validation_passed = False
        error_message = "⚠️ Dayachesi saraina amount (Amount > 0) enter cheyandi!"
    elif payment_mode == "Enchukondi...":
        validation_passed = False
        error_message = "⚠️ Dayachesi 'Payment Mode' ni sarigga enchukondi!"
    elif category == "Enchukondi...":
        validation_passed = False
        error_message = "⚠️ Dayachesi 'Category' ni sarigga enchukondi!"
    elif not description.strip():
        validation_passed = False
        error_message = "⚠️ Description rayadam marchipoyaru! Dayachesi vivaralu nimpandi."

    if not validation_passed:
        st.error(error_message)
    else:
        formatted_date = date.strftime("%d-%m-%Y")
        formatted_month = date.strftime("%B %Y")

        new_row = {
            "S NO": next_sno,
            "Date": formatted_date,
            "Month": formatted_month,
            "Transaction Type": trans_type,
            "Category": category,
