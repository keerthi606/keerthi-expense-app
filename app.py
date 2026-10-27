import pandas as pd
import os
from io import BytesIO
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Keerthi Monthly Expenses Tracker", page_icon="💰", layout="centered"
)

# Header
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
                padding: 15px; border-radius: 12px; text-align: center;">
        <h2 style="color: white; margin: 0;">🌟 KEERTHI MONTHLY EXPENSES TRACKER 🌟</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Data File Setup
DATA_FILE = "expense_data.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(
        columns=[
            "S.No",
            "Date",
            "Transaction Type",
            "Category",
            "Amount",
            "Payment Mode",
            "Description",
        ]
    )

st.write("---")
st.subheader("📝 కొత్త ట్రాన్సాక్షన్ జోడించండి")

# Auto-generate Serial Number
next_sno = int(df["S.No"].max() + 1) if not df.empty else 1

col1, col2 = st.columns(2)

with col1:
    s_no = st.number_input("S NO *", value=next_sno, disabled=True)
    date = st.date_input("Date *")
    tx_type = st.radio(
        "Transaction Type *",
        ["INCOME", "EXPENSE"],
        horizontal=True,
    )

with col2:
    amount = st.number_input(
        "AMOUNT (₹) *", min_value=0.0, step=10.0, format="%.2f"
    )
    payment_mode = st.selectbox(
        "Payment Mode *",
        ["Select Mode", "GOOGLE PAY", "PHONEPE", "PAYTM", "CASH", "BANK TRANSFER"],
    )

    if tx_type == "INCOME":
        categories = ["ఓపెనింగ్ బ్యాలెన్స్", "జీతం (Salary)", "ఇతర ఆదాయం"]
    else:
        categories = [
            "కిరాణా (Groceries)",
            "కరెంట్ బిల్లు",
            "రూమ్ రెంట్",
            "షాపింగ్",
            "మెడికల్",
            "ఇతర ఖర్చులు",
        ]

    category = st.selectbox("Category *", ["Select Category"] + categories)

description = st.text_input(
    "Description (ఎవరికి/దేనికి చెల్లించారు?) *",
    placeholder="ఉదాహరణ: రామయ్య గారికి కిరాణా సామాన్లకు",
)

# Save Transaction
if st.button("💾 Save Transaction", use_container_width=True):
    # Mandatory Validation Checks
    if amount <= 0:
        st.error("⚠️ దయచేసి చెల్లుబాటు అయ్యే అమౌంట్ (Amount) నమోదు చేయండి!")
    elif payment_mode == "Select Mode":
        st.error("⚠️ దయచేసి 'Payment Mode' ఎంచుకోండి!")
    elif category == "Select Category":
        st.error("⚠️ దయచేసి 'Category' ఎంచుకోండి!")
    elif not description.strip():
        st.error(
            "⚠️ దయచేసి 'Description' బాక్స్‌లో వివరాలు నమోదు చేయండి (ఎవరికి ఇచ్చారో రాయండి)!"
        )
    else:
        new_data = pd.DataFrame(
            [
                {
                    "S.No": s_no,
                    "Date": date.strftime("%Y-%m-%d"),
                    "Transaction Type": tx_type,
                    "Category": category,
                    "Amount": amount,
                    "Payment Mode": payment_mode,
                    "Description": description.strip(),
                }
            ]
        )

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ ట్రాన్సాక్షన్ విజయవంతంగా సేవ్ చేయబడింది!")
        st.rerun()

st.write("---")

# Metrics Display
total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
balance = total_income - total_expense

m1, m2, m3 = st.columns(3)
m1.metric("💰 Total Income", f"₹{total_income:,.2f}")
m2.metric("💸 Total Expense", f"₹{total_expense:,.2f}")
m3.metric("⚖️ Balance", f"₹{balance:,.2f}")

st.write("---")
st.subheader("📊 రిపోర్ట్స్ & డేటా పరిశీలన")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Convert DataFrame to Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Monthly_Expenses", index=False)

    st.download_button(
        label="📥 Download as Excel (ఎక్సెల్ రిపోర్ట్ డౌన్‌లోడ్ చేయండి)",
        data=buffer.getvalue(),
        file_name="Keerthi_Monthly_Expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
else:
    st.info("ఇంకా ఎటువంటి ట్రాన్సాక్షన్లు నమోదు చేయలేదు.")
