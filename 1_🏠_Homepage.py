import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stocks prediction",
    page_icon="💰",
)

st.header("🔍 Stock Information")

# --- Sidebar Navigation ---
st.sidebar.page_link("1_🏠_Homepage.py", label="Homepage")
st.sidebar.page_link("2_prediction.py", label="Stock Prediction")

# --- Stock Ticker Input ---
ticker_symbol = st.text_input("Enter Stock Ticker", "AAPL", help="Enter a valid stock ticker symbol, e.g., GOOG, MSFT, TSLA")

if ticker_symbol:
    try:
        # --- Get Ticker Information ---
        company = yf.Ticker(ticker_symbol)
        
        # --- Fetch Historical Data ---
        # Get data for the last 3 months
        data = company.history(period="3mo")

        if data.empty:
            st.warning(f"No historical data found for '{ticker_symbol}'. Please check the ticker symbol.")
        else:
            # --- Display Company Information ---
            st.write(f"### {company.info.get('longName', ticker_symbol)}")
            
            # Show long business summary if available
            if 'longBusinessSummary' in company.info:
                st.write(company.info['longBusinessSummary'])
            else:
                st.info("No business summary available for this company.")

            # --- Display Historical Data ---
            st.write("#### Historical Data (last 3 months)")
            st.dataframe(data)

            # --- Display Line Chart ---
            st.write("#### Stock Price Chart")
            st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"An error occurred: {e}. Please make sure the ticker symbol is correct.")