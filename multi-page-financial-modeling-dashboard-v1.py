import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Function to read financial data from an uploaded Excel file
def load_financial_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Function to identify and extract quarters from column headers
def get_quarters(df):
    return [col for col in df.columns if col.startswith('Q')]

# Function to build income statement model
def build_income_statement(df, quarters):
    income_model = {}
    income_model['Model_Net_Income'] = df[df['A'] == 'Model NI'][quarters].values[0] if not df[df['A'] == 'Model NI'].empty else np.nan
    income_model['Reported_Net_Income'] = df[df['A'] == 'Reported NI'][quarters].values[0] if not df[df['A'] == 'Reported NI'].empty else np.nan
    income_model['D&A'] = df[df['A'] == 'D&A'][quarters].values[0] if not df[df['A'] == 'D&A'].empty else np.nan
    income_model['SBC'] = df[df['A'] == 'SBC'][quarters].values[0] if not df[df['A'] == 'SBC'].empty else np.nan
    income_model['Total_Customers'] = df[df['A'] == 'Total Customers'][quarters].values[0] if not df[df['A'] == 'Total Customers'].empty else np.nan
    income_model['ARPU'] = df[df['A'] == 'ARPU'][quarters].values[0] if not df[df['A'] == 'ARPU'].empty else np.nan
    income_model['Commercial_Revenue'] = df[df['A'] == 'Commercial'][quarters].values[0] if not df[df['A'] == 'Commercial'].empty else np.nan
    income_model['Government_Revenue'] = df[df['A'] == 'Government'][quarters].values[0] if not df[df['A'] == 'Government'].empty else np.nan
    income_model['Revenue'] = (income_model.get('Commercial_Revenue', np.zeros(len(quarters))) + 
                              income_model.get('Government_Revenue', np.zeros(len(quarters))))
    income_model['COGS'] = df[df['A'] == 'COGS'][quarters].values[0] if not df[df['A'] == 'COGS'].empty else np.nan
    income_model['Gross_Profit'] = df[df['A'] == 'Gross Profit'][quarters].values[0] if not df[df['A'] == 'Gross Profit'].empty else np.nan
    income_model['S&M'] = df[df['A'] == 'S&M'][quarters].values[0] if not df[df['A'] == 'S&M'].empty else np.nan
    income_model['R&D'] = df[df['A'] == 'R&D'][quarters].values[0] if not df[df['A'] == 'R&D'].empty else np.nan
    income_model['G&A'] = df[df['A'] == 'G&A'][quarters].values[0] if not df[df['A'] == 'G&A'].empty else np.nan
    income_model['Operating_Income'] = df[df['A'] == 'OpInc'][quarters].values[0] if not df[df['A'] == 'OpInc'].empty else np.nan
    income_model['Interest'] = df[df['A'] == 'Interest'][quarters].values[0] if not df[df['A'] == 'Interest'].empty else np.nan
    income_model['Pretax_Income'] = df[df['A'] == 'Pretax Income'][quarters].values[0] if not df[df['A'] == 'Pretax Income'].empty else np.nan
    income_model['Taxes'] = df[df['A'] == 'Taxes'][quarters].values[0] if not df[df['A'] == 'Taxes'].empty else np.nan
    income_model['Net_Income'] = df[df['A'] == 'Net Income'][quarters].values[0] if not df[df['A'] == 'Net Income'].empty else np.nan
    income_model['EPS'] = df[df['A'] == 'EPS'][quarters].values[0] if not df[df['A'] == 'EPS'].empty else np.nan
    income_model['Shares'] = df[df['A'] == 'SHARES'][quarters].values[0] if not df[df['A'] == 'SHARES'].empty else np.nan
    income_model['Customers_yly'] = df[df['A'] == 'Customers yly'][quarters].values[0] if not df[df['A'] == 'Customers yly'].empty else np.nan
    income_model['ARPU_yly'] = df[df['A'] == 'ARPU yly'][quarters].values[0] if not df[df['A'] == 'ARPU yly'].empty else np.nan
    income_model['Commercial_yly'] = df[df['A'] == 'Commercial yly'][quarters].values[0] if not df[df['A'] == 'Commercial yly'].empty else np.nan
    income_model['Government_yly'] = df[df['A'] == 'Government yly'][quarters].values[0] if not df[df['A'] == 'Government yly'].empty else np.nan
    return income_model

# Function to build balance sheet model
def build_balance_sheet(df, quarters):
    balance_model = {}
    balance_model['Debt'] = df[df['A'] == 'Debt'][quarters].values[0] if not df[df['A'] == 'Debt'].empty else np.nan
    balance_model['Stockholders_Equity'] = df[df['A'] == 'S/E'][quarters].values[0] if not df[df['A'] == 'S/E'].empty else np.nan
    balance_model['Net_Cash'] = df[df['A'] == 'Net Cash'][quarters].values[0] if not df[df['A'] == 'Net Cash'].empty else np.nan
    balance_model['AR'] = df[df['A'] == 'AR'][quarters].values[0] if not df[df['A'] == 'AR'].empty else np.nan
    balance_model['PP&E'] = df[df['A'] == 'PP&E'][quarters].values[0] if not df[df['A'] == 'PP&E'].empty else np.nan
    balance_model['Lease'] = df[df['A'] == 'Lease'][quarters].values[0] if not df[df['A'] == 'Lease'].empty else np.nan
    balance_model['Other_Assets'] = df[df['A'] == 'Other Assets'][quarters].values[0] if not df[df['A'] == 'Other Assets'].empty else np.nan
    balance_model['Assets'] = df[df['A'] == 'Assets'][quarters].values[0] if not df[df['A'] == 'Assets'].empty else np.nan
    balance_model['AVP'] = df[df['A'] == 'AVP'][quarters].values[0] if not df[df['A'] == 'AVP'].empty else np.nan
    balance_model['Accrued'] = df[df['A'] == 'Accrued'][quarters].values[0] if not df[df['A'] == 'Accrued'].empty else np.nan
    balance_model['D/R'] = df[df['A'] == 'D/R'][quarters].values[0] if not df[df['A'] == 'D/R'].empty else np.nan
    balance_model['Deposits'] = df[df['A'] == 'Deposits'][quarters].values[0] if not df[df['A'] == 'Deposits'].empty else np.nan
    return balance_model

# Function to build cash flow model
def build_cash_flow_model(df, quarters):
    cash_flow_model = {}
    cash_flow_model['Cash_Flow_From_Operations'] = df[df['A'] == 'CFFO'][quarters].values[0] if not df[df['A'] == 'CFFO'].empty else np.nan
    cash_flow_model['Purchases_of_Securities'] = df[df['A'] == 'Purchases of Securities'][quarters].values[0] if not df[df['A'] == 'Purchases of Securities'].empty else np.nan
    cash_flow_model['Free_Cash_Flow_Calc'] = (cash_flow_model.get('Cash_Flow_From_Operations', np.zeros(len(quarters))) - 
                                             abs(cash_flow_model.get('Purchases_of_Securities', np.zeros(len(quarters)))))
    cash_flow_model['CFFF'] = df[df['A'] == 'CFFF'][quarters].values[0] if not df[df['A'] == 'CFFF'].empty else np.nan
    cash_flow_model['FX'] = df[df['A'] == 'FX'][quarters].values[0] if not df[df['A'] == 'FX'].empty else np.nan
    cash_flow_model['Cash_Increase'] = df[df['A'] == 'Cash Increase'][quarters].values[0] if not df[df['A'] == 'Cash Increase'].empty else np.nan
    cash_flow_model['FCF'] = df[df['A'] == 'FCF'][quarters].values[0] if not df[df['A'] == 'FCF'].empty else np.nan
    return cash_flow_model

# Function to build operational metrics model
def build_operational_model(df, quarters):
    operational_model = {}
    operational_model['ARPU_yly'] = df[df['A'] == 'ARPU yly'][quarters].values[0] if not df[df['A'] == 'ARPU yly'].empty else np.nan
    operational_model['Revenue_yly'] = df[df['A'] == 'Revenue yly'][quarters].values[0] if not df[df['A'] == 'Revenue yly'].empty else np.nan
    operational_model['Gross_Margin'] = df[df['A'] == 'Gross Margin'][quarters].values[0] if not df[df['A'] == 'Gross Margin'].empty else np.nan
    operational_model['Operating_Margin'] = df[df['A'] == 'Operating Margin'][quarters].values[0] if not df[df['A'] == 'Operating Margin'].empty else np.nan
    operational_model['Tax_Rate'] = df[df['A'] == 'Tax Rate'][quarters].values[0] if not df[df['A'] == 'Tax Rate'].empty else np.nan
    operational_model['Headcount'] = df[df['A'] == 'Headcount'][quarters].values[0] if not df[df['A'] == 'Headcount'].empty else np.nan
    operational_model['Headcount_y/y'] = df[df['A'] == 'Headcount y/y'][quarters].values[0] if not df[df['A'] == 'Headcount y/y'].empty else np.nan
    return operational_model

# Function to extend model for valuation
def valuation_model(net_income, fcf, eps, shares, growth_rate=0.05, discount_rate=0.1, years=5):
    valuation = {}
    cash_flows = fcf if fcf.any() else net_income
    if cash_flows.any():
        terminal_value = cash_flows[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
        cash_flows_list = [cf * (1 + growth_rate) for cf in cash_flows[:-1]]
        cash_flows_list.append(terminal_value / ((1 + discount_rate) ** (years - 1)))
        dcf_value = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows_list, 1))
        valuation['DCF'] = dcf_value
    else:
        valuation['DCF'] = np.nan
    
    if eps.any() and shares.any():
        pe_ratio = 15  # Assume a standard P/E ratio (adjust based on industry)
        pe_value = eps[-1] * shares[-1] * pe_ratio
        valuation['P/E'] = pe_value
    else:
        valuation['P/E'] = np.nan
    
    return valuation

# Function to create and download Excel file
def create_download_link(df_dict, filename="multi_page_financial_model.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for name, df in df_dict.items():
            df.to_excel(writer, sheet_name=name)
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
    return href

import base64

# Streamlit app
st.title("Multi-Page Financial Modeling Dashboard")

# File uploader
uploaded_files = st.file_uploader("Upload Excel files (one per company/page)", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    financial_models = {}
    for uploaded_file in uploaded_files:
        st.subheader(f"Processing: {uploaded_file.name}")
        
        # Load data
        df = load_financial_data(uploaded_file)
        if df is None:
            continue

        # Get quarters
        quarters = get_quarters(df)

        # Build financial models
        income_statement = build_income_statement(df, quarters)
        balance_sheet = build_balance_sheet(df, quarters)
        cash_flow = build_cash_flow_model(df, quarters)
        operational_model = build_operational_model(df, quarters)

        # Combine all models
        financial_model = {**income_statement, **balance_sheet, **cash_flow, **operational_model}

        # Perform valuation
        valuation = valuation_model(
            financial_model.get('Net_Income', np.array([np.nan] * len(quarters))),
            financial_model.get('FCF', np.array([np.nan] * len(quarters))),
            financial_model.get('EPS', np.array([np.nan] * len(quarters))),
            financial_model.get('Shares', np.array([np.nan] * len(quarters)))
        )
        financial_model['Valuation_DCF'] = valuation.get('DCF', np.nan)
        financial_model['Valuation_PE'] = valuation.get('P/E', np.nan)

        # Display results
        st.write(f"### Financial Model for {uploaded_file.name}")
        for key, value in financial_model.items():
            st.write(f"{key}: {value}")

        # Add charts
        if 'Net_Income' in financial_model and not np.isnan(financial_model['Net_Income']).all():
            st.line_chart(pd.DataFrame({'Net Income': financial_model['Net_Income']}, index=quarters))
        if 'FCF' in financial_model and not np.isnan(financial_model['FCF']).all():
            st.line_chart(pd.DataFrame({'Free Cash Flow': financial_model['FCF']}, index=quarters))

        # Store model for download
        financial_models[uploaded_file.name] = pd.DataFrame(financial_model, index=quarters)

    # Download button
    st.markdown(create_download_link(financial_models, "multi_page_financial_model.xlsx"), unsafe_allow_html=True)

else:
    st.write("Please upload at least one Excel file to begin.")

# Run the app with: streamlit run your_script_name.py
