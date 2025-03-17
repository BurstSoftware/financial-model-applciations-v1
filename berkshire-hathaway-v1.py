import pandas as pd
import yfinance as yf
import streamlit as st
from google.cloud import language_v1
import requests

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
    income_stmt = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    return income_stmt, balance_sheet, cash_flow

# Function to generate the report
def generate_report(ticker):
    """Generates a financial report and saves it to an Excel file."""
    
    # Fetch financial data
    income_stmt, balance_sheet, cash_flow = get_financial_data(ticker)
    
    # Perform sentiment analysis on the latest news headlines (for example)
    news = "Stock market is showing a strong upward trend in Q1 2025, analysts predict growth for major companies."
    sentiment_score, sentiment_magnitude = analyze_sentiment(news)
    
    st.write(f"Sentiment Score for News: {sentiment_score}, Magnitude: {sentiment_magnitude}")
    
    # Save to Excel
    report_filename = f"{ticker}_financials.xlsx"
    writer = pd.ExcelWriter(report_filename, engine="xlsxwriter")
    income_stmt.to_excel(writer, sheet_name="Income Statement")
    balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
    cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")
    
    # Summary sheet
    summary = pd.DataFrame({
        "Sentiment Score": [sentiment_score],
        "Sentiment Magnitude": [sentiment_magnitude]
    })
    summary.to_excel(writer, sheet_name="Sentiment Analysis")
    
    writer.close()
    st.success(f"Financial report for {ticker} saved as `{report_filename}`.")

# Streamlit App to generate the report
def main():
    st.title("Financial Model with Google AI")
    
    # User inputs
    ticker = st.text_input("Enter the stock ticker (default is BRK-B):", "BRK-B")
    
    if st.button("Generate Financial Report"):
        generate_report(ticker)

if __name__ == "__main__":
    main()
