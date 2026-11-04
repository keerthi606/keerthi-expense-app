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
        if "House" not in df.columns:
            df["House"] = "House 1 (Ma Kutumbham)"
except FileNotFoundError:
    df = pd.DataFrame(
        columns=[
            "S NO",
            "Date",
            "Month",
            "House",
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

# Overall Metrics lekkinchadam (Top section)
if not df.empty:
    total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
    total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
    
    total_cc_expenses = df[
        (df["Transaction Type"] == "EXPENSE")
        & (df["Payment Mode"] == "CREDIT CARD")
    ]["Amount"].sum()
    
    total_bank_expenses = total_expense - total_cc_expenses
    total_bank_balance = total_income - total_bank_expenses

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("💰 Motham Adayam", f"₹ {total_income:,.2f}")
    mcol2.metric(
        "💸 Motham Kharchu", 
        f"₹ {total_expense:,.2f}",
        delta=f"Bank: ₹{total_bank_expenses:,.2f} | CC: ₹{total_cc_expenses:,.2f}",
        delta_color="off"
    )
    mcol3.metric("🏦 Bank Balance", f"₹ {total_bank_balance:,.2f}")
    mcol4.metric("💳 Credit Card Kharchu", f"₹ {total_cc_expenses:,.2f}")
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

    house_choice = st.selectbox(
        "Illu / Property (House / Property) *", 
        ["House 1 (Ma Kutumbham)", "House 2 (Verhe Kutumbham)", "House 3 (Verhe Kutumbham)", "Common / General"]
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
            "House": house_choice,
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
st.subheader("📊 Kharchula Nivedika (Expenses Summary)")

if not df.empty:
    available_months = sorted(df["Month"].unique().tolist(), reverse=True)
    
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        selected_month_filter = st.selectbox(
            "Nivedika kosam nelani ennukondi (Select Month)", available_months
        )
    with fcol2:
        house_filter_options = [
            "Anni Illu (All Houses)", 
            "House 1 (Ma Kutumbham)", 
            "House 2 (Verhe Kutumbham)", 
            "House 3 (Verhe Kutumbham)", 
            "Common / General"
        ]
        selected_house_filter = st.selectbox("Illu variga filter cheyandi", house_filter_options)

    month_filtered_df = df[df["Month"] == selected_month_filter]
    if selected_house_filter != "Anni Illu (All Houses)":
        month_filtered_df = month_filtered_df[month_filtered_df["House"] == selected_house_filter]

    st.write(f"📅 Nela: **{selected_month_filter}** | Illu: **{selected_house_filter}** Vivaralu")
    st.dataframe(month_filtered_df, use_container_width=True)

    # Excel Download
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        month_filtered_df.to_excel(
            writer, sheet_name=f"Expenses", index=False
        )
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="📥 Ee nela nivedikanu Excel lo download chesukondi (Download as Excel)",
        data=excel_data,
        file_name=f"keerthi_expenses_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    # Summary cards based on filter
    m_income = month_filtered_df[month_filtered_df["Transaction Type"] == "INCOME"]["Amount"].sum()
    m_total_expense = month_filtered_df[month_filtered_df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
    
    m_cc_expenses = month_filtered_df[
        (month_filtered_df["Transaction Type"] == "EXPENSE")
        & (month_filtered_df["Payment Mode"] == "CREDIT CARD")
    ]["Amount"].sum()
    
    m_bank_expenses = m_total_expense - m_cc_expenses
    m_bank_balance = m_income - m_bank_expenses

    scol1, scol2, scol3, scol4 = st.columns(4)
    scol1.metric(f"💰 Adayam", f"₹ {m_income:,.2f}")
    scol2.metric(
        f"💸 Kharchu", 
        f"₹ {m_total_expense:,.2f}",
        delta=f"Bank: ₹{m_bank_expenses:,.2f} | CC: ₹{m_cc_expenses:,.2f}",
        delta_color="off"
    )
    scol3.metric(f"🏦 Bank Balance", f"₹ {m_bank_balance:,.2f}")
    scol4.metric(f"💳 CC Kharchu", f"₹ {m_cc_expenses:,.2f}")

    # Item / Category wise analysis section
    st.markdown("---")
    st.subheader("📈 Item / Category variga nelavari visleshana")

    rep_col1, rep_col2 = st.columns(2)
    with rep_col1:
        report_type = st.radio(
            "Rakam enchukondi (Transaction Type)",
            ["EXPENSE", "INCOME"],
            horizontal=True,
            key="item_rep_type",
        )

    sub_df = df[df["Transaction Type"] == report_type]

    if not sub_df.empty:
        all_categories = sorted(sub_df["Category"].unique().tolist())
        with rep_col2:
            selected_cat = st.selectbox(
                "Item / Category ni enchukondi", all_categories, key="item_cat_select"
            )

        cat_filtered_df = sub_df[sub_df["Category"] == selected_cat]

        if not cat_filtered_df.empty:
            st.write(f"👉 **{selected_cat}** ({report_type}) - Nelavari automatic summary:")

            monthly_summary = (
                cat_filtered_df.groupby("Month")["Amount"].sum().reset_index()
            )
            monthly_summary.columns = ["Month (Nela)", "Total Amount (₹)"]

            m_sum_col, m_det_col = st.columns([1, 2])
            with m_sum_col:
                st.dataframe(monthly_summary, use_container_width=True)
                cat_total = cat_filtered_df["Amount"].sum()
                st.info(f"📌 **{selected_cat}** motham: **₹ {cat_total:,.2f}**")

            with m_det_col:
                st.write("📋 **Anni vivaralu (Detailed Entries):**")
                st.dataframe(
                    cat_filtered_df[
                        [
                            "S NO",
                            "Date",
                            "Month",
                            "House",
                            "Description",
                            "Amount",
                            "Payment Mode",
                        ]
                    ],
                    use_container_width=True,
                )
        else:
            st.info("Ee item-ku sambandhinchina entries evi levu.")
    else:
        st.info("Ee vibhagamlo inka entries namodhu cheyaledu.")

    st.markdown("---")
    st.subheader("❌ Thappuga padina entryni tholaginchandi (Delete Entry)")
    del_col1, del_col2 = st.columns([2, 1])
    with del_col1:
        sno_list = [None] + df["S NO"].tolist()
        sno_to_delete = st.selectbox(
            "Tholaginchavalasina S NO ni enchukondi",
            sno_list,
            format_func=lambda x: "Dayachesi S NO enchukondi..." if x is None else f"S NO: {x}",
        )
    with del_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ DELETE ROW"):
            if sno_to_delete is not None:
                df = df[df["S NO"] != sno_to_delete]
                if not df.empty:
                    df["S NO"] = range(1, len(df) + 1)
                df.to_csv(DATA_FILE, index=False)
                st.success("🗑️ Entry vijayavantamga tholaginchabadindi!")
                st.rerun()
            else:
                st.warning("⚠️ Dayachesi tholaginchanduku oka S NO ni enchukondi!")
else:
    st.info("ℹ️ Inthavaraku entuvali entries levu. Kothha transaction jodinchi aarambinchandi!")

# Footer Heading
st.markdown(
    '<div class="footer-text">🙏 Dhanyavadhamulu (ధన్యవాదములు) 🙏</div>',
    unsafe_allow_html=True,
)
