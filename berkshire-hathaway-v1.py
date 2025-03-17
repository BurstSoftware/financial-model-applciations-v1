import pandas as pd
 
import yfinance as yf
 
import streamlit as st
 

import requests
 

 
# Function to get financial data
 

def get_financial_data(ticker):
 

def get_financial_data(ticker, api_key=None):
 
    """Fetch financial data for a given stock ticker."""
 
    stock = yf.Ticker(ticker)
 


@@ -12,6 +13,18 @@ def get_financial_data(ticker):
 
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

@@ -51,17 +64,14 @@ def discounted_cash_flow(ticker, discount_rate=0.1, terminal_growth=0.02):
 
    return dcf_value
 

 
# Function to generate and save the financial report
 

def generate_report(ticker, api_key):
 

def generate_report(ticker, api_key=None):
 
    """Generates a financial report and saves it to an Excel file."""
 

 
    if not api_key:
 

        st.error("API Key is required!")
 

        return
 

        st.error("API Key is required to access external data!")
 

 

    # Display a message confirming the API Key input (Optional)
 

    st.write(f"Using API Key: {api_key}")
 


 

    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)
 

    # Get financial data
 

    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker, api_key)
 

 
    # DCF valuation
 
    dcf_value = discounted_cash_flow(ticker)

@@ -85,10 +95,10 @@ def generate_report(ticker, api_key):
 

 
# Streamlit App
 
def main():
 

    st.title("Berkshire Hathaway Financial Model")
 

    st.title("Financial Model Application")
 

 
    # API Key input by the user
 

    api_key = st.text_input("Enter your API Key:")
 

    api_key = st.text_input("Enter your API Key for external services (if needed):")
 

 
    # Ticker symbol input by the user
 
    ticker = st.text_input("Enter the stock ticker (default is BRK-B):", "BRK-B")
