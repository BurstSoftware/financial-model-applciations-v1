import streamlit as st
import pandas as pd
import os
import pdfplumber
import openpyxl

# Function to extract text from PDFs
def extract_text_from_pdf(uploaded_files):
    extracted_texts = []
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            extracted_texts.append(text)
    return extracted_texts

# Function to read Excel or CSV files
def read_excel_or_csv(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        return None

# Function to generate a simple financial model (placeholder)
def generate_financial_model(df):
    df["Profit Margin (%)"] = (df["Net Income"] / df["Total Revenue"]) * 100
    return df

# Sidebar Navigation
st.sidebar.title("Financial Modeling App")
page = st.sidebar.radio("Navigate", ["Home", "Upload Documents", "Enter Financial Data", "Generate Model", "Export Data"])

# Home Page
if page == "Home":
    st.title("Welcome to the Financial Modeling App")
    st.write("This app allows users to upload financial documents, extract key data, input financial metrics, generate models, and export reports.")

# Upload Page
elif page == "Upload Documents":
    st.title("Upload Financial Documents")
    uploaded_files = st.file_uploader("Upload financial documents (PDF, Excel, CSV)", accept_multiple_files=True)

    if uploaded_files:
        extracted_data = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".pdf"):
                text_data = extract_text_from_pdf([uploaded_file])
                extracted_data.append("\n".join(text_data))
            elif uploaded_file.name.endswith((".csv", ".xlsx")):
                df = read_excel_or_csv(uploaded_file)
                if df is not None:
                    st.write(f"**Extracted Data from {uploaded_file.name}:**")
                    st.dataframe(df)
                    extracted_data.append(df.to_dict())

        if st.button("Save Extracted Data"):
            with open("extracted_data.txt", "w") as f:
                f.write(str(extracted_data))
            st.success("Data saved successfully!")

# Data Entry Page
elif page == "Enter Financial Data":
    st.title("Enter Financial Data Manually")

    # Input fields for financial data
    total_customers = st.number_input("Total Customers", value=0)
    arpu = st.number_input("ARPU ($)", value=0.0)
    commercial_revenue = st.number_input("Commercial Revenue", value=0)
    government_revenue = st.number_input("Government Revenue", value=0)
    total_revenue = st.number_input("Total Revenue", value=0)

    # Expenses
    cogs = st.number_input("Cost of Goods Sold (COGS)", value=0)
    gross_profit = st.number_input("Gross Profit", value=0)
    sales_marketing = st.number_input("Sales & Marketing (S&M)", value=0)
    r_d = st.number_input("Research & Development (R&D)", value=0)
    g_a = st.number_input("General & Administrative (G&A)", value=0)
    opex = st.number_input("Operating Expenses (OpEx)", value=0)

    # Profitability & EPS
    operating_income = st.number_input("Operating Income (OpInc)", value=0)
    interest_expense = st.number_input("Interest Expense", value=0)
    pretax_income = st.number_input("Pretax Income", value=0)
    taxes = st.number_input("Taxes", value=0)
    net_income = st.number_input("Net Income", value=0)
    eps = st.number_input("Earnings Per Share (EPS)", value=0.0)
    shares_outstanding = st.number_input("Shares Outstanding", value=0)

    # Growth Rates
    customers_yoy = st.number_input("Customer Growth y/y (%)", value=0)
    arpu_yoy = st.number_input("ARPU Growth y/y (%)", value=0)
    commercial_yoy = st.number_input("Commercial Revenue Growth y/y (%)", value=0)
    government_yoy = st.number_input("Government Revenue Growth y/y (%)", value=0)

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

# Model Generation Page
elif page == "Generate Model":
    st.title("Generate Financial Model")

    try:
        df = pd.read_csv("financial_data.csv")
        st.write("### User Inputs:")
        st.dataframe(df)

        # Financial Model Computation
        df = generate_financial_model(df)
        st.write("### Generated Financial Model:")
        st.dataframe(df)

        # Save Model
        if st.button("Save Model"):
            df.to_csv("financial_model.csv", index=False)
            st.success("Financial Model Saved!")

    except:
        st.warning("No financial data found. Please enter data first.")

# Export Data Page
elif page == "Export Data":
    st.title("Export Financial Data")

    if os.path.exists("financial_model.csv"):
        with open("financial_model.csv", "rb") as f:
            st.download_button("Download Financial Model", f, file_name="financial_model.csv", mime="text/csv")

    if os.path.exists("financial_data.csv"):
        with open("financial_data.csv", "rb") as f:
            st.download_button("Download Raw Financial Data", f, file_name="financial_data.csv", mime="text/csv")
