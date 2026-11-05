from io import BytesIO
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

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
    </style>
""",
    unsafe_allow_html=True,
)

# 1. Swagatham
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

# Google Sheets Connection using gspread
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

try:
    creds = Credentials.from_service_account_info(
        dict(st.secrets["connections"]["gsheets"]), scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(
        "1P_EY8UX8Iviz3TLv8Ige1SDXEJCn0TkRsX_gSqz0v4"
    ).sheet1
except Exception as e:
    st.error(f"Google Sheets Connection Error: {e}")
    st.stop()

# Load and clean data
try:
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.dropna(how="all")
        if "Date" in df.columns:
            parsed_dates = pd.to_datetime(
                df["Date"], format="mixed", dayfirst=True, errors="coerce"
            )
            df["Date"] = parsed_dates.dt.strftime("%d-%m-%Y")
            df["Month"] = parsed_dates.dt.strftime("%B %Y")
            df = df.dropna(subset=["Date"])
        if "House" not in df.columns:
            df["House"] = "House 1 (Ma Kutumbham)"
    else:
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
except Exception as e:
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

# Save success message
if "show_success" in st.session_state and st.session_state["show_success"]:
    st.success("✅ Save Successfully! Transaction vijayavantamga save aindi.")
    st.toast("🎉 Transaction save aindi!")
    st.session_state["show_success"] = False

st.markdown("---")

# 2. House Selection
st.subheader("🏠 Illu / Property Enchuko (Select House)")
selected_house = st.selectbox(
    "Deyantho pani undho aa illu/property ni enchukondi *",
    [
        "House 1 (Ma Kutumbham)",
        "House 2 (Verhe Kutumbham)",
        "House 3 (Verhe Kutumbham)",
        "Common / General",
    ],
)

st.markdown("---")

# Filter data for selected house
if not df.empty and "House" in df.columns:
    house_df = df[df["House"] == selected_house]
else:
    house_df = pd.DataFrame(columns=df.columns)

# Metrics Display
if not house_df.empty:
    h_income = (
        house_df[house_df["Transaction Type"] == "INCOME"]["Amount"]
        .astype(float)
        .sum()
    )
    h_expense = (
        house_df[house_df["Transaction Type"] == "EXPENSE"]["Amount"]
        .astype(float)
        .sum()
    )

    h_cc_expenses = (
        house_df[
            (house_df["Transaction Type"] == "EXPENSE")
            & (house_df["Payment Mode"] == "CREDIT CARD")
        ]["Amount"]
        .astype(float)
        .sum()
    )

    h_bank_expenses = h_expense - h_cc_expenses
    h_bank_balance = h_income - h_bank_expenses

    st.write(f"📊 **{selected_house}** yokka Samagra Vivaralu:")
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("💰 Motham Adayam", f"₹ {h_income:,.2f}")
    mcol2.metric(
        "💸 Motham Kharchu",
        f"₹ {h_expense:,.2f}",
        delta=f"Bank: ₹{h_bank_expenses:,.2f} | CC: ₹{h_cc_expenses:,.2f}",
        delta_color="off",
    )
    mcol3.metric("🏦 Bank Balance", f"₹ {h_bank_balance:,.2f}")
    mcol4.metric("💳 Credit Card Kharchu", f"₹ {h_cc_expenses:,.2f}")
else:
    st.info(
        f"ℹ️ {selected_house} ki sambandhinchina vivaralu inthavaraku emi levu. Kinda entry jodinchaandi!"
    )

st.markdown("---")

# 4. Add New Transaction
st.subheader(f"📝 {selected_house} koraku Kothha Transaction Jodinchandi")

col1, col2 = st.columns(2)

with col1:
    next_sno = (
        int(df["S NO"].max()) + 1
        if (
            not df.empty
            and "S NO" in df.columns
            and not df["S NO"].isnull().all()
        )
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
        error_message = (
            "⚠️ Description rayadam marchipoyaru! Dayachesi vivaralu nimpandi."
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
            "House": selected_house,
            "Transaction Type": trans_type,
            "Category": category,
            "Description": description.strip(),
            "Amount": amount,
            "Payment Mode": payment_mode,
        }

        updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        updated_df = updated_df.fillna("")

        try:
            sheet.clear()
            sheet.update(
                [updated_df.columns.values.tolist()]
                + updated_df.values.tolist()
            )
            st.session_state["show_success"] = True
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Data save avvadamlo error vachindi: {e}")

st.markdown("---")
st.subheader(f"📊 {selected_house} Kharchula Nivedika (Expenses Summary)")

if not house_df.empty:
    available_months = sorted(house_df["Month"].unique().tolist(), reverse=True)
    selected_month_filter = st.selectbox(
        "Nivedika kosam nelani ennukondi (Select Month)", available_months
    )

    month_filtered_df = house_df[house_df["Month"] == selected_month_filter]

    st.write(
        f"📅 Nela: **{selected_month_filter}** | Illu: **{selected_house}** Vivaralu"
    )
    st.dataframe(month_filtered_df, use_container_width=True)

    # Excel Download
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        month_filtered_df.to_excel(writer, sheet_name="Expenses", index=False)
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label=(
            "📥 Ee nela nivedikanu Excel lo download chesukondi (Download as Excel)"
        ),
        data=excel_data,
        file_name=f"keerthi_expenses_{selected_house}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
