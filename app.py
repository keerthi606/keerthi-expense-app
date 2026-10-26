import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# మరింత కలర్‌ఫుల్ & స్టైలిష్ మోడర్న్ UI స్టైలింగ్ (Colorful Gradients)
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
        font-size: 30px;
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

# కలర్‌ఫుల్ టైటిల్ హెడర్
st.markdown(
    """
    <div class="title-container">
        <p class="title-text">🌟 KEERTHI MONTHLY EXPENSES TRACKER 🌟</p>
    </div>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "expenses_data.csv"

# డేటా లోడ్ చేయడం లేదా కొత్త టేబుల్ క్రియేట్ చేయడం
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

# --- 1. పైభాగంలో కలర్‌ఫుల్ టోటల్స్ కార్డ్స్ ---
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
  next_sno = len(df) + 1 if df.empty else int(df["S NO"].max()) + 1
  st.number_input("S NO *", value=next_sno, disabled=True)
  date = st.date_input("Date")

  trans_type = st.radio(
      "Transaction Type", ["INCOME", "EXPENSE"], horizontal=True
  )

  if trans_type == "INCOME":
    categories = [
        "ఓపెనింగ్ బ్యాలెన్స్",
        "జీతం / వేతనం",
        "క్రెడిట్ కార్డ్",
        "లోన్",
        "అప్పు",
    ]
  else:
    categories = [
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

  category = st.selectbox("Category", categories, key=f"cat_{trans_type}")

with col2:
  amount = st.number_input("AMOUNT (₹)", min_value=0.0, format="%.2f")

  payment_mode = st.selectbox(
      "Payment Mode",
      ["GOOGLE PAY", "PHONE PE", "CASH", "CREDIT CARD", "OTHERS", "BANK ACCOUNT"],
  )

  if payment_mode == "OTHERS":
    description = st.text_area(
        "Other Payment Description (దయచేసి వివరించండి)"
    )
  else:
    description = f"Paid via {payment_mode}"

st.markdown("")
if st.button("💾 SAVE TRANSACTION"):
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
  st.success("🎉 విజయవంతంగా సేవ్ చేయబడింది!")
  st.rerun()

# --- 2. నెలవారీ ఖర్చుల నివేదిక & డౌన్‌లోడ్ ఆప్షన్ ---
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

  # CSV Download Button
  csv_data = month_filtered_df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 ఈ నెల నివేదికను డౌన్‌లోడ్ చేసుకోండి (Download CSV)",
      data=csv_data,
      file_name=f"keerthi_expenses_{selected_month_filter}.csv",
      mime="text/csv",
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

  # --- 3. ఐటమ్ మరియు నెలవారీ విశ్లేషణ ---
  st.markdown("---")
  st.subheader("📈 ఐటమ్ మరియు నెలవారీ విశ్లేషణ (Item & Month-wise Report)")

  report_type = st.radio(
      "విశ్లేషణ రకం ఎంచుకోండి", ["EXPENSE", "INCOME"], horizontal=True
  )

  sub_df = df[df["Transaction Type"] == report_type]

  if not sub_df.empty:
    all_categories = sub_df["Category"].unique().tolist()
    selected_cat = st.selectbox(
        "ఒక ఐటమ్ / కేటగిరీని ఎంచుకోండి", all_categories, key="report_cat"
    )

    cat_filtered_df = sub_df[sub_df["Category"] == selected_cat]

    if not cat_filtered_df.empty:
      st.write(
          f"### 👉 **{selected_cat}** ({report_type}) యొక్క నెలవారీ వివరాలు:"
      )

      monthly_summary = (
          cat_filtered_df.groupby("Month")["Amount"].sum().reset_index()
      )
      monthly_summary.columns = ["Month (నెల)", "Total Amount (₹)"]

      st.dataframe(monthly_summary, use_container_width=True)

      cat_total = cat_filtered_df["Amount"].sum()
      st.info(
          f"📌 **{selected_cat}** మీద మొత్తం పెట్టిన {report_type}:"
          f" **₹ {cat_total:,.2f}**"
      )
    else:
      st.info("ఈ ఐటమ్‌కు సంబంధించిన ఎంట్రీలు ఏవీ లేవు.")
  else:
    st.info("ఈ విభాగంలో ఎంట్రీలు లేవు.")

  # --- 4. Payment Mode Wise Report ---
  st.markdown("---")
  st.subheader("💳 పేమెంట్ మోడ్ వారీగా విశ్లేషణ (Payment Mode Report)")

  pay_modes = df["Payment Mode"].unique().tolist()
  selected_mode = st.selectbox("ఒక పేమెంట్ మోడ్‌ని ఎంచుకోండి", pay_modes)

  mode_filtered_df = df[df["Payment Mode"] == selected_mode]
  if not mode_filtered_df.empty:
    st.dataframe(mode_filtered_df, use_container_width=True)
    mode_total = mode_filtered_df["Amount"].sum()
    st.info(
        f"📌 **{selected_mode}** ద్వారా జరిగిన మొత్తం ట్రాన్సాక్షన్స్ విలువ:"
        f" **₹ {mode_total:,.2f}**"
    )

  # --- 5. సురక్షితమైన డిలీట్ ఆప్షన్ ---
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
        st.success(f"🗑️ S NO {sno_to_delete} విజయవంతంగా తొలగించబడింది!")
        st.rerun()
      else:
        st.warning("⚠️ దయచేసి తొలగించడానికి ఒక S NO ని ఎంచుకోండి!")
else:
  st.info(
      "ℹ️ ఇంతవరకు ఎటువంటి ఎంట్రీలు లేవు. కొత్త ట్రాన్సాక్షన్ జోడించి ప్రారంభించండి!"
  )
