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

# Month-wise mariyu Overall Metrics lekkinchadam
if not df.empty:
    available_months = sorted(df["Month"].unique().tolist(), reverse=True)
    selected_month_filter = st.selectbox(
        "Nivedika kosam nelani ennukondi (Select Month)", available_months
    )

    month_filtered_df = df[df["Month"] == selected_month_filter]

    # Selected month income & expenses
    m_income = month_filtered_df[month_filtered_df["Transaction Type"] == "INCOME"]["Amount"].sum
