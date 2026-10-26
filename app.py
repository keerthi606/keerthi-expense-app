import pandas as pd
import streamlit as st

st.title("KEERTHI MONTHLY EXPENSE APP")

DATA_FILE = "expenses_data.csv"

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
      ]
  )

with st.form("expense_form"):
  st.subheader("కొత్త ట్రాన్సాక్షన్ జోడించండి")

  date = st.date_input("తేదీ (Date)")
  trans_type = st.selectbox("రకం (Transaction Type)", ["INCOME", "EXPENSE"])
  category = st.selectbox(
      "కేటగిరీ (Category)",
      ["ఆహారం (Food)", "ప్రయాణం (Travel)", "బిల్లులు (Bills)", "జీతం (Salary)", "ఇతరములు"],
  )
  description = st.text_area("వివరణ (Description)")
  amount = st.number_input("మొత్తం (Amount)", min_value=0.0, format="%.2f")

  submitted = st.form_submit_button("సేవ్ చేయి (Save)")

  if submitted:
    new_id = len(df) + 1
    new_row = {
        "S NO": new_id,
        "Date": str(date),
        "Transaction Type": trans_type,
        "Category": category,
        "Description": description,
        "Amount": amount,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("విజయవంతంగా సేవ్ చేయబడింది!")

st.subheader("ఖర్చుల నివేదిక (Expenses List)")
if not df.empty:
  st.dataframe(df)

  total_income = df[df["Transaction Type"] == "INCOME"]["Amount"].sum()
  total_expense = df[df["Transaction Type"] == "EXPENSE"]["Amount"].sum()
  balance = total_income - total_expense

  col1, col2, col3 = st.columns(3)
  col1.metric("మొత్తం ఆదాయం (Income)", f"₹{total_income}")
  col2.metric("మొత్తం ఖర్చు (Expense)", f"₹{total_expense}")
  col3.metric("మిగులు (Balance)", f"₹{balance}")
else:
  st.info("ఇంతవరకు ఎటువంటి ఎంట్రీలు లేవు.")