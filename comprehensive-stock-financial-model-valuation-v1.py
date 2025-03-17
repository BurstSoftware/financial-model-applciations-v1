import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

# Title of the Streamlit App
st.title("Comprehensive Stock Financial Model & Valuation")

# User input for multiple stock tickers
tickers = st.text_input("Enter Stock Tickers (comma-separated, e.g., AAPL, BRK-B, TSLA):", "BRK-B, AAPL")

# User-defined financial parameters
discount_rate = st.slider("Select Discount Rate (%)", 8, 15, 10) / 100
terminal_growth = st.slider("Select Terminal Growth Rate (%)", 0, 3, 1) / 100
years = st.slider("Projection Years", 5, 10, 5)

def get_financial_data(ticker):
    """Fetches financial statements and key metrics from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        key_stats = stock.info
        return income_stmt, balance_sheet, cash_flow, key_stats
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None

def forecast_cash_flows(ticker, years, growth_rate):
    """Forecasts cash flows based on historical trends."""
    try:
        stock = yf.Ticker(ticker)
        cash_flows = stock.cashflow.loc["Total Cash From Operating Activities"]
        last_cf = cash_flows.iloc[0]

        projected_cf = [last_cf * (1 + growth_rate) ** i for i in range(1, years + 1)]
        return projected_cf
    except Exception as e:
        st.error(f"Forecasting Error for {ticker}: {e}")
        return None

def discounted_cash_flow(ticker, discount_rate, terminal_growth, years):
    """Performs a multi-scenario DCF valuation."""
    try:
        base_growth = 0.05
        optimistic_growth = base_growth + 0.03
        pessimistic_growth = base_growth - 0.02

        scenarios = {
            "Base Case": base_growth,
            "Optimistic Case": optimistic_growth,
            "Pessimistic Case": pessimistic_growth
        }
        
        valuations = {}
        for scenario, growth in scenarios.items():
            projected_cf = forecast_cash_flows(ticker, years, growth)
            if projected_cf is None:
                return None

            dcf_value = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected_cf, 1))
            terminal_value = (projected_cf[-1] * (1 + terminal_growth)) / (discount_rate - terminal_growth)
            dcf_value += terminal_value / ((1 + discount_rate) ** years)
            valuations[scenario] = dcf_value

        return valuations
    except Exception as e:
        st.error(f"DCF Calculation Error for {ticker}: {e}")
        return None

def peer_comparison(ticker):
    """Compares key financial ratios to industry peers."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "Market Cap": info.get("marketCap"),
            "PE Ratio": info.get("trailingPE"),
            "EV/EBITDA": info.get("enterpriseValue") / info.get("ebitda") if info.get("ebitda") else None,
            "Debt to Equity": info.get("debtToEquity"),
            "Return on Equity (ROE)": info.get("returnOnEquity"),
            "Price to Book (P/B)": info.get("priceToBook")
        }
    except Exception as e:
        st.error(f"Error fetching peer comparison data for {ticker}: {e}")
        return None

def generate_report(ticker, discount_rate, terminal_growth, years):
    """Generates an Excel financial report for a given stock."""
    try:
        income_stmt, balance_sheet, cash_flow, key_stats = get_financial_data(ticker)
        valuations = discounted_cash_flow(ticker, discount_rate, terminal_growth, years)
        ratios = peer_comparison(ticker)

        if valuations is None or ratios is None:
            return None

        writer = pd.ExcelWriter(f"{ticker}_financials.xlsx", engine="xlsxwriter")
        income_stmt.to_excel(writer, sheet_name="Income Statement")
        balance_sheet.to_excel(writer, sheet_name="Balance Sheet")
        cash_flow.to_excel(writer, sheet_name="Cash Flow Statement")

        valuation_df = pd.DataFrame(valuations.items(), columns=["Scenario", "DCF Valuation"])
        valuation_df.to_excel(writer, sheet_name="Valuation Scenarios")

        ratios_df = pd.DataFrame(ratios.items(), columns=["Metric", "Value"])
        ratios_df.to_excel(writer, sheet_name="Peer Comparison")

        writer.close()
        return f"{ticker}_financials.xlsx"
    except Exception as e:
        st.error(f"Report Generation Error for {ticker}: {e}")
        return None

# Loop through multiple stocks
ticker_list = [t.strip().upper() for t in tickers.split(",")]

for ticker in ticker_list:
    if st.button(f"Generate Financial Model for {ticker}"):
        income_stmt, balance_sheet, cash_flow, key_stats = get_financial_data(ticker)

        if income_stmt is not None:
            st.subheader(f"Financial Statements for {ticker}")
            st.subheader("Income Statement")
            st.write(income_stmt)

            st.subheader("Balance Sheet")
            st.write(balance_sheet)

            st.subheader("Cash Flow Statement")
            st.write(cash_flow)

            valuations = discounted_cash_flow(ticker, discount_rate, terminal_growth, years)
            if valuations:
                st.subheader(f"DCF Valuation for {ticker}")
                st.write(pd.DataFrame(valuations.items(), columns=["Scenario", "Estimated Value ($)"]))

            ratios = peer_comparison(ticker)
            if ratios:
                st.subheader(f"Peer Comparison for {ticker}")
                st.write(pd.DataFrame(ratios.items(), columns=["Metric", "Value"]))

            report_file = generate_report(ticker, discount_rate, terminal_growth, years)
            if report_file:
                with open(report_file, "rb") as file:
                    st.download_button(label=f"Download {ticker} Report",
                                       data=file,
                                       file_name=report_file,
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Run with:
# streamlit run app.py
