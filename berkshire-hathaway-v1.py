import pandas as pd
import requests
import yfinance as yf

# Constants
API_KEY = "your_api_key"  # Replace with your actual API key
COMPANY = "BRK-B"  # Default to Berkshire Hathaway

def get_financial_data(ticker):
    """Fetch financial data for a given stock ticker."""
    stock = yf.Ticker(ticker)
    
    # Get financial statements
    income_stmt = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    return income_stmt, balance_sheet, cash_flow

def discounted_cash_flow(ticker, discount_rate=0.1, terminal_growth=0.02):
    """Perform a simple DCF valuation."""
    stock = yf.Ticker(ticker)
    cash_flows = stock.cashflow.loc["Total Cash From Operating Activities"]
    
    # Project future cash flows (assuming constant growth)
    projected_cf = [cash_flows.iloc[0] * (1 + terminal_growth) ** i for i in range(1, 6)]
    
    # Discount future cash flows
    dcf_value = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected_cf, 1))
    
    return dcf_value

def generate_report(ticker):
    """Generates a financial report and saves it to an Excel file."""
    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)
    
    # DCF valuation
    dcf_value = discounted_cash_flow(ticker)
    
    # Save to Excel
    writer = pd.ExcelWriter(f"{ticker}_financials.xlsx", engine="xlsxwriter")
    income_stmt.to_excel(writer, sheet_name="Income Statement")
    balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
    cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")
    
    # Summary sheet
    summary = pd.DataFrame({"DCF Valuation": [dcf_value]})
    summary.to_excel(writer, sheet_name="Summary")
    
    writer.close()
    print(f"Financial report for {ticker} saved.")

# Example Usage
generate_report(COMPANY)
