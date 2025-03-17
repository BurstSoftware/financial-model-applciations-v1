import pandas as pd

 
import yfinance as yf
 
import streamlit as st
 

from google.cloud import language_v1
 
import requests
 

 

# Function to get financial data
 

def get_financial_data(ticker, api_key=None):
 

# Set up the Natural Language API client
 

client = language_v1.LanguageServiceClient()
 


 

# Function to get sentiment analysis for financial news
 

def analyze_sentiment(text):
 

    """Analyze the sentiment of a given text using Google Cloud Natural Language API."""
 

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
 

    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
 

    
 

    return sentiment.score, sentiment.magnitude
 


 

# Function to fetch financial data from Yahoo Finance (yfinance)
 

def get_financial_data(ticker):
 
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
 

# Function to generate the report
 

def generate_report(ticker):
 
    """Generates a financial report and saves it to an Excel file."""
 

 

    if not api_key:
 

        st.error("API Key is required to access external data!")
 

    # Fetch financial data
 

    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)
 

 

    # Get financial data
 

    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker, api_key)
 

    # Perform sentiment analysis on the latest news headlines (for example)
 

    news = "Stock market is showing a strong upward trend in Q1 2025, analysts predict growth for major companies."
 

    sentiment_score, sentiment_magnitude = analyze_sentiment(news)
 

 

    # DCF valuation
 

    dcf_value = discounted_cash_flow(ticker)
 

    if dcf_value is None:
 

        st.error(f"Could not calculate DCF value for {ticker}.")
 

        return
 

    st.write(f"Sentiment Score for News: {sentiment_score}, Magnitude: {sentiment_magnitude}")
 

 
    # Save to Excel
 
    report_filename = f"{ticker}_financials.xlsx"

@@ -87,25 +45,24 @@ def generate_report(ticker, api_key=None):
 
    cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")
 

 
    # Summary sheet
 

    summary = pd.DataFrame({"DCF Valuation": [dcf_value]})
 

    summary.to_excel(writer, sheet_name="Summary")
 

    summary = pd.DataFrame({
 

        "Sentiment Score": [sentiment_score],
 

        "Sentiment Magnitude": [sentiment_magnitude]
 

    })
 

    summary.to_excel(writer, sheet_name="Sentiment Analysis")
 

 
    writer.close()
 
    st.success(f"Financial report for {ticker} saved as `{report_filename}`.")
 

 

# Streamlit App
 

# Streamlit App to generate the report
 
def main():
 

    st.title("Financial Model Application")
 

    
 

    # API Key input by the user
 

    api_key = st.text_input("Enter your API Key for external services (if needed):")
 

    st.title("Financial Model with Google AI")
 

 

    # Ticker symbol input by the user
 

    # User inputs
 
    ticker = st.text_input("Enter the stock ticker (default is BRK-B):", "BRK-B")
 

 

    # Button to generate the report
 
    if st.button("Generate Financial Report"):
 

        generate_report(ticker, api_key)
 

        generate_report(ticker)
 

 
if __name__ == "__main__":
 
    main()
