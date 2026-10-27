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

# UI Styling
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
        color: #555555;
        font-size: 16px;
        font-weight: 600;
        margin-top: 40px;
        padding: 15px;
        border-top: 2px dashed #ccc;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Modati lo Swagatham
st.markdown("### 🙏 **Swagatham** 🙏")

st.markdown(
    """
    <div class="title-container">
        <p class="title-text">🌟 KEERTHI MONTHLY EXPENSES TRACKER 🌟</p>
    </div>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "expenses_data.csv"

# డేటా లోడ్ చేయడం మరియు dayfirst=True తో సరైన డేట్/నెల ఫార్మాట్‌లోకి మార్చడం
try:
    df = pd.read_csv(DATA_FILE)
    if not df.empty and "Date" in df.columns:
        # dayfirst=True pettadam valla day mundu, month tarvata correct ga parse avutundi
        parsed_dates = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["Date"] = parsed_dates.dt.strftime("%d-%m-%Y")
        df["Month"] = parsed_dates.dt.strftime("%B %Y")
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

if not df.empty:
    total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
    total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
    balance = total_income - total_expense

    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("💰 మొత్తం ఆదాయం (Income)", f"₹ {total_income:,.2f}")
    mcol2.metric("💸 మొత్తం ఖర్చు (Expense)", f"₹ {total_expense:,.2f}")
    mcol3.metric("⚖️ మిగులు (Balance)", f"₹ {balance:,.2f}")
    st.markdown("---")

st.subheader("📝 కొత్త ట్రాన్సాక్షన్ జోడించండి")

col1, col2 = st.columns(2)

with col1:
    next_sno = (
        int(df["S NO"].max()) + 1
        if (not df.empty and "S NO" in df.columns and not df["S NO"].isnull().all())
        else 1
    )
    st.number_input(
        "S NO * (ఆటోమేటిక్)", value=next_sno, disabled=True, key="auto_sno"
    )

    date = st.date_input("Date *")
    formatted_date_preview = date.strftime("%d-%m-%Y")
    st.caption(f"📅 ఎంచుకున్న తేదీ రూపం: **{formatted_date_preview}**")

    trans_type = st.radio(
        "Transaction Type *", ["INCOME", "EXPENSE"], horizontal=True
    )

    if trans_type == "INCOME":
        categories = [
            "ఎంచుకోండి...",
            "ఓపెనింగ్ బ్యాలెన్స్",
            "జీతం / వేతనం",
            "క్రెడిట్ కార్డ్",
            "లోన్",
            "అప్పు",
            "ఇతర ఆదాయం",
        ]
    else:
        categories = [
            "ఎంచుకోండి...",
            "సరుకులు",
            "కూరగాయలు / పండ్లు",
            "పాలు",
            "పెరుగు",
            "పెట్రోలు",
            "క్రెడిట్ కార్డ్ పేమెంట్",
            "వెహికల్ మెయింటెనెన్స్",
            "అప్పు",
            "డ్వాక్రా లోను",
            "కరెంట్ బిల్లు",
            "పేపర్ బిల్లు",
            "టిఫిన్స్ / హోటల్",
            "మూవీస్",
            "క్లోత్స్",
            "టాయిస్",
            "మందులు / మెడికల్",
            "మొబైల్ రీఛార్జ్ / డిష్ / ఇంటర్నెట్",
            "స్కూల్ / కాలేజ్ ఫీజులు",
            "ఇంటి అద్దె (House Rent)",
            "సిలిండర్ / గ్యాస్ బిల్లు",
            "వాటర్ బిల్లు / క్యాన్లు",
            "పూజ సామాగ్రి",
            "ఇతరాలు",
        ]

    category = st.selectbox("Category *", categories, key=f"cat_{trans_type}")

with col2:
    amount = st.number_input(
        "AMOUNT (₹) *", min_value=0.0, step=1.0, format="%.2f"
    )

    payment_modes = [
        "ఎంచుకోండి...",
        "GOOGLE PAY",
        "PHONE PE",
        "CASH",
        "CREDIT CARD",
        "BANK ACCOUNT",
        "OTHERS",
    ]
    payment_mode = st.selectbox("Payment Mode *", payment_modes)

    description = st.text_input(
        "Description (ఎవరికి/దేనికి చెల్లించారు?) *",
        placeholder="ఉదాహరణ: రామయ్య గారికి కిరాణా సామాన్లకు",
    )

st.markdown("")

if st.button("💾 SAVE TRANSACTION"):
    validation_passed = True
    error_message = ""

    if amount <= 0:
        validation_passed = False
        error_message = (
            "⚠️ దయచేసి సరైన అమౌంట్ (Amount > 0) ఎంటర్ చేయండి!"
        )
    elif payment_mode == "ఎంచుకోండి...":
        validation_passed = False
        error_message = "⚠️ దయచేసి 'Payment Mode' ని సరిగ్గా ఎంచుకోండి!"
    elif category == "ఎంచుకోండి...":
        validation_passed = False
        error_message = "⚠️ దయచేసి 'Category' ని సరిగ్గా ఎంచుకోండి!"
    elif not description.strip():
        validation_passed = False
        error_message = (
            "⚠️ డిస్క్రిప్షన్ రాయడం మర్చిపోయారు! దయచేసి ఎవరికి/దేనికి"
            " ఇచ్చారో రాయండి."
        )

    if not validation_passed:
        st.error(error_message)
    else:
        formatted_date = date.strftime("%d-%m-%Y")
        formatted_month = date.strftime("%B %Y")  # ఉదాహరణకు: August 2026

        new_row = {
            "S NO": next_sno,
            "Date": formatted_date,
            "Month": formatted_month,
            "Transaction Type": trans_type,
            "Category": category,
            "Description": description.strip(),
            "Amount": amount,
            "Payment Mode": payment_mode,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success(
            "✅ Save Successfully! ట్రాన్సాక్షన్ విజయవంతంగా సేవ్ చేయబడింది."
        )
        st.balloons()
        st.rerun()

st.markdown("---")
st.subheader("📊 ఖర్చుల నివేదిక (Expenses Summary)")

if not df.empty:
    available_months = sorted(df["Month"].unique().tolist(), reverse=True)
    selected_month_filter = st.selectbox(
        "నివేదిక కోసం నెలని ఎంచుకోండి (Select Month)", available_months
    )

    month_filtered_df = df[df["Month"] == selected_month_filter]

    st.write(f"📅 నెల: **{selected_month_filter}** వివరాలు")
    st.dataframe(month_filtered_df, use_container_width=True)

    # Excel Download
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        month_filtered_df.to_excel(
            writer, sheet_name=f"Expenses", index=False
        )
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label=(
            "📥 ఈ నెల నివేదికను ఎక్సెల్ లో డౌన్‌లోడ్ చేసుకోండి (Download as"
            " Excel)"
        ),
        data=excel_data,
        file_name=f"keerthi_expenses_{selected_month_filter}.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        use_container_width=True,
    )

    m_income = month_filtered_df[month_filtered_df["Transaction Type"] == "INCOME"][
        "Amount"
    ].sum()
    m_expense = month_filtered_df[
        month_filtered_df["Transaction Type"] == "EXPENSE"
    ]["Amount"].sum()
    m_balance = m_income - m_expense

    scol1, scol2, scol3 = st.columns(3)
    scol1.metric(f"💰 {selected_month_filter} ఆదాయం", f"₹ {m_income:,.2f}")
    scol2.metric(f"💸 {selected_month_filter} ఖర్చు", f"₹ {m_expense:,.2f}")
    scol3.metric(f"⚖️ {selected_month_filter} మిగులు", f"₹ {m_balance:,.2f}")

    st.markdown("---")
    st.subheader("❌ తప్పుగా పడిన ఎంట్రీని తొలగించండి (Delete Entry)")
    del_col1, del_col2 = st.columns([2, 1])
    with del_col1:
        sno_list = [None] + df["S NO"].tolist()
        sno_to_delete = st.selectbox(
            "తొలగించవలసిన S NO ని ఎంచుకోండి",
            sno_list,
            format_func=lambda x: "దయచేసి S NO ఎంచుకోండి..."
            if x is None
            else f"S NO: {x}",
        )
    with del_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ DELETE ROW"):
            if sno_to_delete is not None:
                df = df[df["S NO"] != sno_to_delete]
                if not df.empty:
                    df["S NO"] = range(1, len(df) + 1)
                df.to_csv(DATA_FILE, index=False)
                st.success("🗑️ ఎంట్రీ విజయవంతంగా తొలగించబడింది!")
                st.rerun()
            else:
                st.warning("⚠️ దయచేసి తొలగించడానికి ఒక S NO ని ఎంచుకోండి!")
else:
    st.info(
        "ℹ️ ఇంతవరకు ఎటువంటి ఎంట్రీలు లేవు. కొత్త ట్రాన్సాక్షన్ జోడించి"
        " ప్రారంభించండి!"
    )

# Chivaralo Dhanyavadhamulu
st.markdown(
    '<div class="footer-text">🙏 <b>Dhanyavadhamulu</b> 🙏</div>',
    unsafe_allow_html=True,
)
