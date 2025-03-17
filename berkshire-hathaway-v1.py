import pandas as pd
import yfinance as yf
import streamlit as st
import requests

# Function to get financial data
def get_financial_data(ticker, api_key=None):
    """Fetch financial data for a given stock ticker."""
    stock = yf.Ticker(ticker)
    
    # Get financial statements
    income_stmt = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    # If we have an API key and need to fetch external data via API, do it here
    if api_key:
        # Example of using API key for an external service (e.g., Alpha Vantage, etc.)
        # Replace this with the actual external API logic you need
        url = f"https://api.example.com/data?apikey={api_key}&symbol={ticker}"
        response = requests.get(url)
        if response.status_code == 200:
            external_data = response.json()
            st.write(f"External Data for {ticker}: {external_data}")
        else:
            st.error(f"Failed to fetch external data for {ticker} using the API key.")
    
    return income_stmt, balance_sheet, cash_flow

# Function to perform discounted cash flow (DCF) valuation
def discounted_cash_flow(ticker, discount_rate=0.1, terminal_growth=0.02):
    """Perform a simple DCF valuation."""
    stock = yf.Ticker(ticker)
    cash_flows = stock.cashflow
    
    # Print the entire cash flow data for debugging purposes
    print("Cash Flow Data:")
    print(cash_flows)

    # Look for common cash flow labels and select the appropriate one
    possible_keys = [
        'Total Cash From Operating Activities',
        'Operating Cash Flow',
        'Net Cash Provided by Operating Activities'
    ]
    
    cash_flow_data = None
    for key in possible_keys:
        if key in cash_flows.index:
            cash_flow_data = cash_flows.loc[key]
            print(f"Using cash flow key: {key}")
            break
    
    if cash_flow_data is None:
        print(f"None of the expected cash flow keys found in data for {ticker}")
        return None

    # Project future cash flows (assuming constant growth)
    projected_cf = [cash_flow_data.iloc[0] * (1 + terminal_growth) ** i for i in range(1, 6)]
    
    # Discount future cash flows
    dcf_value = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected_cf, 1))
    
    return dcf_value

# Function to generate and save the financial report
def generate_report(ticker, api_key=None):
    """Generates a financial report and saves it to an Excel file."""
    
    if not api_key:
        st.error("API Key is required to access external data!")
    
    # Get financial data
    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker, api_key)
    
    # DCF valuation
    dcf_value = discounted_cash_flow(ticker)
    if dcf_value is None:
        st.error(f"Could not calculate DCF value for {ticker}.")
        return
    
    # Save to Excel
    report_filename = f"{ticker}_financials.xlsx"
    writer = pd.ExcelWriter(report_filename, engine="xlsxwriter")
    income_stmt.to_excel(writer, sheet_name="Income Statement")
    balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
    cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")
    
    # Summary sheet
    summary = pd.DataFrame({"DCF Valuation": [dcf_value]})
    summary.to_excel(writer, sheet_name="Summary")
    
    writer.close()
    st.success(f"Financial report for {ticker} saved as `{report_filename}`.")

# Streamlit App
def main():
    st.title("Financial Model Application")
    
    # API Key input by the user
    api_key = st.text_input("Enter your API Key for external services (if needed):")
    
    # Ticker symbol input by the user
    ticker = st.text_input("Enter the stock ticker (default is BRK-B):", "BRK-B")
    
    # Button to generate the report
    if st.button("Generate Financial Report"):
        generate_report(ticker, api_key)

if __name__ == "__main__":
    main()
