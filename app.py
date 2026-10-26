import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Keerthi Monthly Expense Tracker",
    page_icon="💰",
    layout="wide",
)

# App chala colourful ga undadaniki custom CSS styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #ff2222;
        color: white;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🌟 KEERTHI MONTHLY EXPENSE APP 🌟")
st.markdown("---")

DATA_FILE = "expenses_data.csv"

# Data load cheyadam leda kotha table create cheyadam
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

st.subheader("📝 Kotha Transaction Jodinchandi")

# Two columns ga form layout set chedham
col1, col2 = st.columns(2)

with col1:
  next_sno = len(df) + 1
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

  category = st.selectbox("Category", categories)

with col2:
  amount = st.number_input("AMOUNT (₹)", min_value=0.0, format="%.2f")

  # Payment mode select chesinappudu options
  payment_mode = st.radio(
      "Payment Mode",
      ["GOOGLE PAY", "PHONE PE", "CASH", "CREDIT CARD", "OTHERS", "BANK ACCOUNT"],
      horizontal=True,
  )

  # "OTHERS" select chesinappudu matrame description kanipistundi
  if payment_mode == "OTHERS":
    description = st.text_area(
        "Other Payment Description (దయచేసి వివరించండి)"
    )
  else:
    description = (
        f"Paid via {payment_mode}"  # Default ga payment mode save avutundi
    )

st.markdown("")
if st.button("💾 SAVE TRANSACTION"):
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
  st.success("🎉 Vijayavanthanga save cheyabadindi!")
  st.rerun()

# Nivedika / Summary Vibhagam
st.markdown("---")
st.subheader("📊 Kharchula Nivedika (Expenses Summary)")

if not df.empty:
  st.dataframe(df, use_container_width=True)

  total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
  total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
  balance = total_income - total_expense

  mcol1, mcol2, mcol3 = st.columns(3)
  mcol1.metric("💰 Mottam Adayam (Income)", f"₹{total_income:,.2f}")
  mcol2.metric("💸 Mottam Kharchu (Expense)", f"₹{total_expense:,.2f}")
  mcol3.metric("⚖️ Migulu (Balance)", f"₹{balance:,.2f}")
else:
  st.info(
      "ℹ️ Inthavaraku entrulem levu. Kotha transaction add chesi start"
      " cheyandi!"
  )
