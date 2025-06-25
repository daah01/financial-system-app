# Daahir's Personal Financial System – Project Blueprint

# -------------------------------
# STREAMLIT APP: budget_tracker_app.py
# -------------------------------

# This Streamlit app allows Daahir to interact with his budget system from his phone.
# It wraps the BudgetTracker module with input fields, displays, and export options.

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import matplotlib.pyplot as plt

class BudgetTracker:
    def __init__(self, income, fixed_expenses, variable_expenses, month=None, year=None):
        self.income = income
        self.fixed_expenses = fixed_expenses
        self.variable_expenses = variable_expenses
        self.timestamp = datetime.now()
        self.month = month or self.timestamp.month
        self.year = year or self.timestamp.year

    def total_expenses(self):
        return sum(self.fixed_expenses.values()) + sum(self.variable_expenses.values())

    def surplus(self):
        return self.income - self.total_expenses()

    def summary(self):
        return {
            "Month": f"{self.month}/{self.year}",
            "Income": self.income,
            "Fixed Expenses": self.fixed_expenses,
            "Variable Expenses": self.variable_expenses,
            "Total Expenses": self.total_expenses(),
            "Surplus": self.surplus()
        }

    def to_dataframe(self):
        return pd.DataFrame({
            'Category': ['Income'] + list(self.fixed_expenses.keys()) + list(self.variable_expenses.keys()) + ['Surplus'],
            'Amount': [self.income] + list(self.fixed_expenses.values()) + list(self.variable_expenses.values()) + [self.surplus()]
        })

    def to_json(self):
        return json.dumps(self.summary(), indent=4)

# Streamlit UI Starts Here
st.title("📊 Daahir's Budget Tracker")

month = st.selectbox("Select Month", options=list(range(1, 13)), index=datetime.now().month - 1)
year = st.number_input("Enter Year", value=datetime.now().year)
income = st.number_input("Monthly Income (NOK)", value=50000)

st.markdown("### Fixed Expenses")
fixed_expenses = {}
for label in ["Rent", "Loan Payments", "Utilities"]:
    fixed_expenses[label] = st.number_input(f"{label}", value=0, key=f"fixed_{label}")

st.markdown("### Variable Expenses")
variable_expenses = {}
for label in ["Groceries", "Leisure", "Transport"]:
    variable_expenses[label] = st.number_input(f"{label}", value=0, key=f"var_{label}")

if st.button("Generate Budget Summary"):
    tracker = BudgetTracker(income, fixed_expenses, variable_expenses, month, year)
    st.success("✅ Summary Generated")
    st.write(tracker.to_dataframe())
    st.markdown("### 💡 Insights")
    st.markdown(f"**Total Expenses:** {tracker.total_expenses()} NOK")
    st.markdown(f"**Surplus:** {tracker.surplus()} NOK")

    st.download_button(
        label="Download JSON",
        data=tracker.to_json(),
        file_name="budget_summary.json",
        mime="application/json"
    )

    # Add visualizations
    st.markdown("### 📊 Budget Bar Chart")
    st.bar_chart(tracker.to_dataframe().set_index("Category"))

    expense_df = pd.DataFrame({
        'Category': list(tracker.fixed_expenses.keys()) + list(tracker.variable_expenses.keys()),
        'Amount': list(tracker.fixed_expenses.values()) + list(tracker.variable_expenses.values())
    })

    if not expense_df.empty and expense_df['Amount'].sum() > 0:
        st.markdown("### 🥧 Expense Distribution")
        fig, ax = plt.subplots()
        ax.pie(expense_df["Amount"], labels=expense_df["Category"], autopct='%1.1f%%')
        st.pyplot(fig)
    else:
        st.info("Enter expense values to see pie chart.")
