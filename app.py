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

# స్వాగతం హెడ్డింగ్
st.markdown(
    '<div class="welcome-text">🙏 స్వాగతం (Swagatham) 🙏</div>',
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

# డేటా లోడ్ చేయడం మరియు తేదీలు/నెలలను సరిగ్గా సెట్ చేయడం
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

# సేవ్ సక్సెస్ మెసేజ్ చూపించడం
if "show_success" in st.session_state and st.session_state["show_success"]:
    st.success("✅ Save Successfully! ట్రాన్సాక్షన్ విజయవంతంగా సేవ్ చేయబడింది.")
    st.toast("🎉 ట్రాన్సాక్షన్ సేవ్ అయింది!")
    st.session_state["show_success"] = False

# బ్యాలెన్స్ లెక్కించడం (క్రెడిట్ కార్డ్ మరియు బ్యాంక్ అకౌంట్ వేరుగా)
if not df.empty:
    # మొత్తం ఆదాయం
    total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()

    # సాధారణ ఖర్చులు (క్రెడిట్ కార్డ్ కాకుండా వాడిన క్యాష్/ఫోన్‌పే/బ్యాంక్)
    non_cc_expenses = df[
        (df["Transaction Type"] == "EXPENSE")
        & (df["Payment Mode"] != "CREDIT CARD")
    ]["Amount"].sum()

    # నెట్ బ్యాంక్/క్యాష్ బ్యాలెన్స్
    actual_cash_bank_balance = total_income - non_cc_expenses

    # క్రెడిట్ కార్డ్ ద్వారా చేసిన ఖర్చులు (అవుట్‌స్టాండింగ్ బిల్లు)
    cc_spent = df[
        (df["Transaction Type"] == "EXPENSE")
        & (df["Payment Mode"] == "CREDIT CARD")
    ]["Amount"].sum()

    # క్రెడిట్ కార్డ్ బిల్లు చెల్లింపులు (క్యాష్ లేదా బ్యాంక్ నుండి కట్టినవి)
    cc_payments = df[
        (df["Transaction Type"] == "EXPENSE")
        & (df["Category"] == "క్రెడిట్ కార్డ్ పేమెంట్")
    ]["Amount"].sum()

    # ప్రస్తుత క్రెడిట్ కార్డ్ బాకీ
    current_cc_due = cc_spent - cc_payments

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("💰 మొత్తం ఆదాయం", f"₹ {total_income:,.2f}")
    mcol2.metric(
        "🏦 బ్యాంక్ / క్యాష్ బ్యాలెన్స్", f"₹ {actual_cash_bank_balance:,.2f}"
    )
    mcol3.metric(
        "💳 క్రెడిట్ కార్డ్ బిల్లు బాకీ", f"₹ {current_cc_due:,.2f}"
    )
    mcol4.metric(
        "💸 మొత్తం ఖర్చులు",
        f"₹ {df[df['Transaction Type'] == 'EXPENSE']['Amount'].sum():,.2f}",
    )
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
            "ఇంటి రుణం (Home Loan)",
            "ద్విచక్ర వాహన రుణం (Bike Loan)",
            "కరెంట్ బిల్లు",
            "పేపర్ బిల్లు",
            "టిఫిన్స్ / హోటల్",
            "మూవీస్ / వినోదం",
            "క్లోత్స్ / దుస్తులు",
            "టాయిస్ / ఆటబొమ్మలు",
            "మందులు / మెడికల్",
            "మొబైల్ రీఛార్జ్ / డిష్ / ఇంటర్నెట్",
            "స్కూల్ / కాలేజ్ ఫీజులు",
            "ఇంటి అద్దె (House Rent)",
            "సిలిండర్ / గ్యాస్ బిల్లు",
            "వాటర్ బిల్లు / క్యాన్లు",
            "పూజా సామాగ్రి",
            "ప్రయాణ ఖర్చులు (Travel Expenses)",
            "బాబు పాకెట్ మనీ (Babu Pocket Money)",
            "పాపా పాకెట్ మనీ (Papa Pocket Money)",
            "నాన్న పాకెట్ మనీ (Nanna Pocket Money)",
            "అమ్మ పాకెట్ మనీ (Amma Pocket Money)",
            "మరమ్మతులు (Repairs & Maintenance)",
            "విరాళాలు (Donations / Charity)",
            "శీతల పానీయాలు (Cool Drinks / Beverages)",
            "చికెన్ / మటన్ / చేపలు (Chicken/Mutton/Fish)",
            "గుడ్లు (Eggs)",
            "ఇన్సూరెన్స్ / ఎల్‌ఐసి (Insurance Premium)",
            "డ్రై ఫ్రూట్స్ (Dry Fruits & Nuts)",
            "శుభకార్యాలు / బహుమతులు (Gifts & Functions)",
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
            "⚠️ డిస్క్రిప్షన్ రాయడం మర్చిపోయారు! దయచేసి వివరాలు నింపండి."
        )

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
            "Description": description.strip(),
            "Amount": amount,
            "Payment Mode": payment_mode,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.session_state["show_success"] = True
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
