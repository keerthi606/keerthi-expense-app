import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# Professional & Clean Modern UI Styling (No heart symbols, elegant dark/gold & gradient theme)
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        height: 50px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #162c54 0%, #1e3c72 100%);
        color: white;
    }
    .title-container {
        background: linear-gradient(90deg, #f857a6 0%, #ff5858 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    .title-text {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: 1px;
        margin: 0;
    }
    h2, h3 {
        color: #2c3e50;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Clean title without heart symbols
st.markdown(
    """
    <div class="title-container">
        <p class="title-text">KEERTHI MONTHLY EXPENSES TRACKER</p>
    </div>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "expenses_data.csv"

# Data load cheyadam leda kotha table create cheyadam
try:
  df = pd.read_csv(DATA_FILE)
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime(
        "%Y-%m-%d"
    )
  if "Month" not in df.columns and "Date" in df.columns:
    df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")
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

# --- 1. Top lo Totals chupinchadam ---
if not df.empty:
  total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
  total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
  balance = total_income - total_expense

  mcol1, mcol2, mcol3 = st.columns(3)
  mcol1.metric("Mottam Adayam (Income)", f"Rs. {total_income:,.2f}")
  mcol2.metric("Mottam Kharchu (Expense)", f"Rs. {total_expense:,.2f}")
  mcol3.metric("Migulu (Balance)", f"Rs. {balance:,.2f}")
  st.markdown("---")

st.subheader("Kotha Transaction Jodinchandi")

col1, col2 = st.columns(2)

with col1:
  next_sno = len(df) + 1 if df.empty else int(df["S NO"].max()) + 1
  st.number_input("S NO *", value=next_sno, disabled=True)
  date = st.date_input("Date")

  trans_type = st.radio(
      "Transaction Type", ["INCOME", "EXPENSE"], horizontal=True
  )

  if trans_type == "INCOME":
    categories = [
        "Open Balance",
        "Salary / Wages",
        "Credit Card",
        "Loan",
        "Borrowings",
    ]
  else:
    categories = [
        "Groceries (Sarukulu)",
        "Vegetables / Fruits",
        "Milk",
        "Curd",
        "Petrol",
        "Credit Card Payment",
        "Vehicle Maintenance",
        "Debt Repayment",
        "DWACRA Loan",
        "Current Bill",
        "Paper Bill",
        "Tiffins / Hotel",
        "Movies",
        "Clothes",
        "Toys",
        "Medical / Pharmacy",
        "Mobile Recharge / Dish / Internet",
        "School / College Fees",
        "House Rent",
        "Gas Cylinder",
        "Water Bill / Cans",
        "Pooja Items",
        "Others",
    ]

  category = st.selectbox("Category", categories, key=f"cat_{trans_type}")

with col2:
  amount = st.number_input("AMOUNT (Rs.)", min_value=0.0, format="%.2f")

  payment_mode = st.selectbox(
      "Payment Mode",
      ["GOOGLE PAY", "PHONE PE", "CASH", "CREDIT CARD", "OTHERS", "BANK ACCOUNT"],
  )

  if payment_mode == "OTHERS":
    description = st.text_area("Other Payment Description")
  else:
    description = f"Paid via {payment_mode}"

st.markdown("")
if st.button("SAVE TRANSACTION"):
  selected_month = date.strftime("%Y-%m")
  new_row = {
      "S NO": next_sno,
      "Date": str(date),
      "Month": selected_month,
      "Transaction Type": trans_type,
      "Category": category,
      "Description": description,
      "Amount": amount,
      "Payment Mode": payment_mode,
  }
  df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
  df.to_csv(DATA_FILE, index=False)
  st.success("Vijayavanthanga save cheyabadindi!")
  st.rerun()

# --- 2. Month-wise Expenses Summary Report ---
st.markdown("---")
st.subheader("Kharchula Nivedika (Monthly Summary)")

if not df.empty:
  available_months = sorted(df["Month"].unique().tolist(), reverse=True)
  selected_month_filter = st.selectbox(
      "Nivedika kosam nelani enchukondi", available_months
  )

  month_filtered_df = df[df["Month"] == selected_month_filter]

  st.write(f"Nela: **{selected_month_filter}** Vivaralu")
  st.dataframe(month_filtered_df, use_container_width=True)

  m_income = month_filtered_df[month_filtered_df["Transaction Type"] == "INCOME"][
      "Amount"
  ].sum()
  m_expense = month_filtered_df[
      month_filtered_df["Transaction Type"] == "EXPENSE"
  ]["Amount"].sum()
  m_balance = m_income - m_expense

  scol1, scol2, scol3 = st.columns(3)
  scol1.metric(f"{selected_month_filter} Income", f"Rs. {m_income:,.2f}")
  scol2.metric(f"{selected_month_filter} Expense", f"Rs. {m_expense:,.2f}")
  scol3.metric(f"{selected_month_filter} Balance", f"Rs. {m_balance:,.2f}")

  # --- 3. Item & Month-wise Analysis (Income / Expense separate) ---
  st.markdown("---")
  st.subheader("Item mariyu Nelavari Visleshana (Item & Month-wise Report)")

  report_type = st.radio(
      "Visleshana Rakam Enchukondi",
      ["EXPENSE", "INCOME"],
      horizontal=True,
  )

  sub_df = df[df["Transaction Type"] == report_type]

  if not sub_df.empty:
    all_categories = sub_df["Category"].unique().tolist()
    selected_cat = st.selectbox(
        "Oka Item / Category ni enchukondi", all_categories, key="report_cat"
    )

    cat_filtered_df = sub_df[sub_df["Category"] == selected_cat]

    if not cat_filtered_df.empty:
      st.write(f"**{selected_cat}** ({report_type}) yokka nelavari vivaralu:")

      monthly_summary = (
          cat_filtered_df.groupby("Month")["Amount"].sum().reset_index()
      )
      monthly_summary.columns = ["Month", "Total Amount (Rs.)"]

      st.dataframe(monthly_summary, use_container_width=True)

      cat_total = cat_filtered_df["Amount"].sum()
      st.info(f"**{selected_cat}** meda mottam pettina kharchu: Rs. {cat_total:,.2f}")
    else:
      st.info("Ee item-ku sambandhinchina entries evi levu.")
  else:
    st.info("Ee vibhagamlo entries levu.")

  # --- 4. NEW FEATURE: Payment Mode Wise Report ---
  st.markdown("---")
  st.subheader("Payment Mode Wise Analysis (GPay / PhonePe / Cash Report)")

  pay_modes = df["Payment Mode"].unique().tolist()
  selected_mode = st.selectbox("Oka Payment Mode ni enchukondi", pay_modes)

  mode_filtered_df = df[df["Payment Mode"] == selected_mode]
  if not mode_filtered_df.empty:
    st.dataframe(mode_filtered_df, use_container_width=True)
    mode_total = mode_filtered_df["Amount"].sum()
    st.info(
        f"**{selected_mode}** dwara jarigina mottam transactions value: Rs."
        f" {mode_total:,.2f}"
    )

  # --- 5. Safe Delete Entry Option ---
  st.markdown("---")
  st.subheader("Thappuga padina entry ni tholaginchandi (Delete Entry)")
  del_col1, del_col2 = st.columns([2, 1])
  with del_col1:
    sno_list = [None] + df["S NO"].tolist()
    sno_to_delete = st.selectbox(
        "Tholaginchavalasina S NO ni enchukondi",
        sno_list,
        format_func=lambda x: "Dayachesi S NO enchukondi..."
        if x is None
        else f"S NO: {x}",
    )
  with del_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("DELETE ROW"):
      if sno_to_delete is not None:
        df = df[df["S NO"] != sno_to_delete]
        if not df.empty:
          df["S NO"] = range(1, len(df) + 1)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"S NO {sno_to_delete} vijayavanthanga tholaginchabadindi!")
        st.rerun()
      else:
        st.warning("Dayachesi tholaginchadaniki oka S NO ni enchukondi!")
else:
  st.info(
      "Inthavaraku entrulem levu. Kotha transaction add chesi start cheyandi!"
  )
