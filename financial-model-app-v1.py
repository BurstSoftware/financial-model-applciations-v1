import streamlit as st
import pandas as pd

# App navigation
st.sidebar.title("Financial Model App")
page = st.sidebar.radio("Navigate", ["Home", "Enter Financial Data", "Model Output"])

# Home Page
if page == "Home":
    st.title("Welcome to the Financial Modeling App")
    st.write("This app allows users to input financial data and generate a complete financial model.")

# Input Page
elif page == "Enter Financial Data":
    st.title("Enter Financial Data")

    st.subheader("Balance Sheet Inputs")
    debt = st.number_input("Debt", value=0)
    other_liabilities = st.number_input("Other Liabilities", value=0)
    s_e = st.number_input("Shareholder Equity (S/E)", value=0)
    lse = st.number_input("Liabilities + Shareholder Equity (L+S/E)", value=0)

    st.subheader("Income Statement Inputs")
    model_ni = st.number_input("Model Net Income", value=0)
    reported_ni = st.number_input("Reported Net Income", value=0)
    d_a = st.number_input("Depreciation & Amortization (D&A)", value=0)
    sbc = st.number_input("Stock-Based Compensation (SBC)", value=0)
    lease = st.number_input("Lease Costs", value=0)
    loss_securities = st.number_input("Loss from Securities", value=0)
    noncash_consideration = st.number_input("Noncash Consideration", value=0)
    other_income_expense = st.number_input("Other Income/Expense", value=0)
    working_capital = st.number_input("Working Capital (WC)", value=0)

    st.subheader("Cash Flow Statement Inputs")
    cffo = st.number_input("Cash Flow from Operations (CFFO)", value=0)
    pp_e = st.number_input("Property, Plant & Equipment (PP&E)", value=0)
    purchase_securities = st.number_input("Purchases of Securities", value=0)
    sales_securities = st.number_input("Sales of Securities", value=0)
    other_cffi = st.number_input("Other Investing Cash Flows (CFFI)", value=0)

    st.subheader("Financing Activities")
    exercise_options = st.number_input("Exercise Options", value=0)
    repurchases = st.number_input("Stock Repurchases", value=0)

    # Save Inputs
    user_data = {
        "Debt": debt,
        "Other Liabilities": other_liabilities,
        "S/E": s_e,
        "L+S/E": lse,
        "Model Net Income": model_ni,
        "Reported Net Income": reported_ni,
        "D&A": d_a,
        "SBC": sbc,
        "Lease": lease,
        "Loss from Securities": loss_securities,
        "Noncash Consideration": noncash_consideration,
        "Other Income/Expense": other_income_expense,
        "Working Capital": working_capital,
        "CFFO": cffo,
        "PP&E": pp_e,
        "Purchases of Securities": purchase_securities,
        "Sales of Securities": sales_securities,
        "Other CFFI": other_cffi,
        "Exercise Options": exercise_options,
        "Repurchases": repurchases,
    }

    if st.button("Save Data"):
        df = pd.DataFrame([user_data])
        df.to_csv("financial_data.csv", index=False)
        st.success("Financial Data Saved!")

# Model Output Page
elif page == "Model Output":
    st.title("Financial Model Output")
    
    try:
        df = pd.read_csv("financial_data.csv")
        st.write("### User Inputs:")
        st.dataframe(df)
        
        # Placeholder for model calculations
        st.write("### Financial Model Results (Coming Soon)")
    except:
        st.warning("No data found. Please enter financial data first.")
