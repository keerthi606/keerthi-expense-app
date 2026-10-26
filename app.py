import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# యాప్ మరింత కలర్‌ఫుల్‌గా, స్టైలిష్‌గా కనిపించడానికి కస్టమ్ CSS
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8e53 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        height: 50px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff2222 0%, #ff6b3b 100%);
        color: white;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h2, h3 {
        color: #2c3e50;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🌟 KEERTHI MONTHLY EXPENSE APP 🌟")
st.markdown("---")

DATA_FILE = "expenses_data.csv"

# డేటా లోడ్ చేయడం లేదా కొత్త టేబుల్ క్రియేట్ చేయడం
try:
  df = pd.read_csv(DATA_FILE)
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
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

st.subheader("📝 కొత్త ట్రాన్సాక్షన్ జోడించండి")

col1, col2 = st.columns(2)

with col1:
  next_sno = len(df) + 1 if df.empty else int(df["S NO"].max()) + 1
  st.number_input("S NO *", value=next_sno, disabled=True)
  date = st.date_input("Date")

  # Transaction Type
  trans_type = st.radio(
      "Transaction Type", ["INCOME", "EXPENSE"], horizontal=True
  )

  # Category Lists
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

  category = st.selectbox("Category", categories)

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

# నివేదిక / సమ్మరీ విభాగం
st.markdown("---")
st.subheader("📊 ఖర్చుల నివేదిక (Expenses Summary)")

if not df.empty:
  # డేటా ఫ్రేమ్ లో తేదీని సరిగ్గా చూపడానికి
  display_df = df.copy()
  if "Month" in display_df.columns:
    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.date

  st.dataframe(display_df, use_container_width=True)

  total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
  total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
  balance = total_income - total_expense

  mcol1, mcol2, mcol3 = st.columns(3)
  mcol1.metric("💰 మొత్తం ఆదాయం (Income)", f"₹{total_income:,.2f}")
  mcol2.metric("💸 మొత్తం ఖర్చు (Expense)", f"₹{total_expense:,.2f}")
  mcol3.metric("⚖️ మిగులు (Balance)", f"₹{balance:,.2f}")

  # --- ఐటమ్ వైస్ & మంత్ వైస్ రిపోర్ట్ (Item-wise & Month-wise Analysis) ---
  st.markdown("---")
  st.subheader("📈 ఐటమ్ మరియు నెలవారీ విశ్లేషణ (Item & Month-wise Report)")

  all_categories = df["Category"].unique().tolist()
  selected_cat = st.selectbox(
      "ఒక ఐటమ్ / కేటగిరీని ఎంచుకోండి (Select Item to Analyze)", all_categories
  )

  # ఫిల్టర్ చేసిన డేటా
  filtered_df = df[df["Category"] == selected_cat]

  if not filtered_df.empty:
    st.write(f"### 👉 **{selected_cat}** యొక్క నెలవారీ వివరాలు:")

    # నెల వారీగా గ్రూప్ చేసి టోటల్ అమౌంట్ కట్టడం
    monthly_summary = (
        filtered_df.groupby("Month")["Amount"].sum().reset_index()
    )
    monthly_summary.columns = ["Month (నెల)", "Total Amount (మొత్తం ఖర్చు ₹)"]

    st.dataframe(monthly_summary, use_container_width=True)

    cat_total = filtered_df["Amount"].sum()
    st.info(
        f"📌 **{selected_cat}** మీద ఇప్పటివరకు పెట్టిన మొత్తం ఖర్చు: **₹{cat_total:,.2f}**"
    )
  else:
    st.info("ఈ ఐటమ్‌కు సంబంధించిన ఎంట్రీలు ఏవీ లేవు.")

  # --- ట్రాన్సాక్షన్ తొలగించే విభాగం (Delete Transaction) ---
  st.markdown("---")
  st.subheader("❌ తప్పుగా పడిన ఎంట్రీని తొలగించండి (Delete Entry)")
  del_col1, del_col2 = st.columns([2, 1])
  with del_col1:
    sno_to_delete = st.selectbox(
        "తొలగించవలసిన S NO ని ఎంచుకోండి", df["S NO"].tolist()
    )
  with del_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ DELETE ROW"):
      df = df[df["S NO"] != sno_to_delete]
      if not df.empty:
        df["S NO"] = range(1, len(df) + 1)
      df.to_csv(DATA_FILE, index=False)
      st.success(f"🗑️ S NO {sno_to_delete} విజయవంతంగా తొలగించబడింది!")
      st.rerun()
else:
  st.info(
      "ℹ️ ఇంతవరకు ఎటువంటి ఎంట్రీలు లేవు. కొత్త ట్రాన్సాక్షన్ జోడించి ప్రారంభించండి!"
  )
