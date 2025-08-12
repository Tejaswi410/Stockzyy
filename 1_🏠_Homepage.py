import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stock Information",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Stock Market Information")

# --- Sidebar Navigation ---
st.sidebar.page_link("1_🏠_Homepage.py", label="Stock Information")
st.sidebar.page_link("pages/2_📈_prediction.py", label="Stock Prediction")

# --- Load Ticker Data ---
@st.cache_data
def load_ticker_data():
    try:
        return pd.read_csv("tickers.csv")
    except FileNotFoundError:
        st.error("The 'tickers.csv' file was not found. Please add it to your repository.")
        return None

tickers_df = load_ticker_data()

if tickers_df is not None:
    # --- Company Selection ---
    company_name = st.selectbox(
        "Search for a company by name",
        tickers_df["Name"],
        help="Select a company to see its stock details."
    )

    if company_name:
        # Get the corresponding ticker symbol
        ticker_symbol = tickers_df[tickers_df["Name"] == company_name]["Ticker"].iloc[0]

        st.info(f"Showing results for: **{company_name} ({ticker_symbol})**")

        try:
            # --- Get Ticker Information ---
            company = yf.Ticker(ticker_symbol)
            data = company.history(period="3mo")

            if data.empty:
                st.warning(f"No historical data found for '{ticker_symbol}'.")
            else:
                # --- Display Company Information ---
                st.write(f"### {company.info.get('longName', company_name)}")
                if 'longBusinessSummary' in company.info:
                    st.write(company.info['longBusinessSummary'])
                else:
                    st.info("No detailed business summary is available for this company.")

                # --- Display Historical Data and Chart ---
                col1, col2 = st.columns(2)

                with col1:
                    st.write("#### Historical Data (last 3 months)")
                    st.dataframe(data)

                with col2:
                    st.write("#### Stock Price Chart")
                    st.line_chart(data['Close'])

        except Exception as e:
            st.error(f"An error occurred: {e}. Please check the ticker symbol or try again later.")