import pandas as pd
import streamlit as st

st.set_page_config(page_title="Monthly Expense Tracker", layout="wide")

st.title("KEERTHI MONTHLY EXPENSE APP")

DATA_FILE = "expenses_data.csv"

# డేటాను లోడ్ చేయడం లేదా కొత్త టేబుల్ క్రియేట్ చేయడం
try:
  df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
  df = pd.DataFrame(
      columns=[
          "S NO",
          "Date",
          "Transaction Type",
          "Category",
          "Description",
          "Amount",
          "Payment Mode",
      ]
  )

with st.form("expense_form"):
  st.subheader("కొత్త ట్రాన్సాక్షన్ జోడించండి")

  # 1. S NO (ఆటో క్యాలిక్యులేటెడ్)
  next_sno = len(df) + 1
  st.number_input("S NO *", value=next_sno, disabled=True)

  # 2. Date
  date = st.date_input("Date")

  # 3. Transaction Type
  trans_type = st.radio("Transaction Type", ["INCOME", "EXPENSE"], horizontal=True)

  # 4. Category (IF Condition లాజిక్)
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

  # 5. Description
  description = st.text_area("Description")

  # 6. Amount
  amount = st.number_input("AMOUNT", min_value=0.0, format="%.2f")

  # 7. Payment Mode
  payment_mode = st.radio(
      "Payment Mode",
      [
          "GOOGLE PAY",
          "PHONE PE",
          "CASH",
          "CREDIT CARD",
          "OTHERS",
          "BANK ACCOUNT",
      ],
  )

  submitted = st.form_submit_button("Save")

  if submitted:
    new_row = {
        "S NO": next_sno,
        "Date": str(date),
        "Transaction Type": trans_type,
        "Category": category,
        "Description": description,
        "Amount": amount,
        "Payment Mode": payment_mode,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("విజయవంతంగా సేవ్ చేయబడింది!")
    st.rerun()

# నివేదిక / సమ్మరీ విభాగం
st.divider()
st.subheader("ఖర్చుల నివేదిక (Expenses List)")

if not df.empty:
  st.dataframe(df, use_container_width=True)

  total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
  total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
  balance = total_income - total_expense

  col1, col2, col3 = st.columns(3)
  col1.metric("మొత్తం ఆదాయం (Income)", f"₹{total_income:,.2f}")
  col2.metric("మొత్తం ఖర్చు (Expense)", f"₹{total_expense:,.2f}")
  col3.metric("మిగులు (Balance)", f"₹{balance:,.2f}")
else:
  st.info("ఇంతవరకు ఎటువంటి ఎంట్రీలు లేవు.")
