import streamlit as st
import pandas as pd

# App Navigation
st.sidebar.title("Financial Model App")
page = st.sidebar.radio("Navigate", ["Home", "Enter Financial Data", "Model Output"])

# Home Page
if page == "Home":
    st.title("Welcome to the Financial Modeling App")
    st.write("This app allows users to input financial data and generate a complete financial model.")

# Input Page
elif page == "Enter Financial Data":
    st.title("Enter Financial Data")

    # Customer & Revenue Inputs
    st.subheader("Customer & Revenue Metrics")
    total_customers = st.number_input("Total Customers", value=0)
    arpu = st.number_input("ARPU ($)", value=0.0)
    commercial_revenue = st.number_input("Commercial Revenue", value=0)
    government_revenue = st.number_input("Government Revenue", value=0)
    total_revenue = st.number_input("Total Revenue", value=0)

    # Cost & Expense Inputs
    st.subheader("Cost & Expense Breakdown")
    cogs = st.number_input("Cost of Goods Sold (COGS)", value=0)
    gross_profit = st.number_input("Gross Profit", value=0)
    sales_marketing = st.number_input("Sales & Marketing (S&M)", value=0)
    r_d = st.number_input("Research & Development (R&D)", value=0)
    g_a = st.number_input("General & Administrative (G&A)", value=0)
    opex = st.number_input("Operating Expenses (OpEx)", value=0)

    # Profitability Inputs
    st.subheader("Profitability & Earnings")
    operating_income = st.number_input("Operating Income (OpInc)", value=0)
    interest_expense = st.number_input("Interest Expense", value=0)
    pretax_income = st.number_input("Pretax Income", value=0)
    taxes = st.number_input("Taxes", value=0)
    net_income = st.number_input("Net Income", value=0)
    eps = st.number_input("Earnings Per Share (EPS)", value=0.0)
    shares_outstanding = st.number_input("Shares Outstanding", value=0)

    # Growth Rates
    st.subheader("Growth Rates & Trends")
    customers_yoy = st.number_input("Customer Growth y/y (%)", value=0)
    arpu_yoy = st.number_input("ARPU Growth y/y (%)", value=0)
    commercial_yoy = st.number_input("Commercial Revenue Growth y/y (%)", value=0)
    government_yoy = st.number_input("Government Revenue Growth y/y (%)", value=0)

    # Save Inputs
    user_data = {
        "Total Customers": total_customers,
        "ARPU": arpu,
        "Commercial Revenue": commercial_revenue,
        "Government Revenue": government_revenue,
        "Total Revenue": total_revenue,
        "COGS": cogs,
        "Gross Profit": gross_profit,
        "Sales & Marketing": sales_marketing,
        "R&D": r_d,
        "G&A": g_a,
        "OpEx": opex,
        "Operating Income": operating_income,
        "Interest Expense": interest_expense,
        "Pretax Income": pretax_income,
        "Taxes": taxes,
        "Net Income": net_income,
        "EPS": eps,
        "Shares Outstanding": shares_outstanding,
        "Customer Growth y/y (%)": customers_yoy,
        "ARPU Growth y/y (%)": arpu_yoy,
        "Commercial Revenue Growth y/y (%)": commercial_yoy,
        "Government Revenue Growth y/y (%)": government_yoy
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
        
        # Placeholder for financial calculations
        st.write("### Financial Model Results (Coming Soon)")
    except:
        st.warning("No data found. Please enter financial data first.")
