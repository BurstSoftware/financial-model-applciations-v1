import streamlit as st
import pandas as pd
import yfinance as yf

# Title of the Streamlit App
st.title("Stock Financial Model & DCF Valuation")

# User input for stock ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, BRK-B):", "BRK-B")

def get_financial_data(ticker):
    """Fetches financial statements from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        return income_stmt, balance_sheet, cash_flow
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None, None

def discounted_cash_flow(ticker, discount_rate=0.1, terminal_growth=0.02):
    """Performs a simple DCF valuation based on operating cash flows."""
    try:
        stock = yf.Ticker(ticker)
        cash_flows = stock.cashflow.loc["Total Cash From Operating Activities"]
        projected_cf = [cash_flows.iloc[0] * (1 + terminal_growth) ** i for i in range(1, 6)]
        dcf_value = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected_cf, 1))
        return dcf_value
    except Exception as e:
        st.error(f"DCF Calculation Error: {e}")
        return None

def generate_report(ticker):
    """Generates an Excel financial report."""
    try:
        income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)
        dcf_value = discounted_cash_flow(ticker)

        writer = pd.ExcelWriter(f"{ticker}_financials.xlsx", engine="xlsxwriter")
        income_stmt.to_excel(writer, sheet_name="Income Statement")
        balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
        cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")
        pd.DataFrame({"DCF Valuation": [dcf_value]}).to_excel(writer, sheet_name="Summary")
        writer.close()
        
        return f"{ticker}_financials.xlsx"
    except Exception as e:
        st.error(f"Report Generation Error: {e}")
        return None

# Fetch financial data
if st.button("Generate Financial Model"):
    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)

    if income_stmt is not None:
        st.subheader("Income Statement")
        st.write(income_stmt)

        st.subheader("Balance Sheet")
        st.write(balance_sheet)

        st.subheader("Cash Flow Statement")
        st.write(cash_flow)

        # Perform DCF Valuation
        dcf_value = discounted_cash_flow(ticker)
        if dcf_value:
            st.subheader("DCF Valuation")
            st.write(f"Estimated Intrinsic Value: **${dcf_value:,.2f}**")

        # Generate Report
        report_file = generate_report(ticker)
        if report_file:
            with open(report_file, "rb") as file:
                st.download_button(label="Download Financial Report",
                                   data=file,
                                   file_name=report_file,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Run the app with:
# streamlit run app.py
