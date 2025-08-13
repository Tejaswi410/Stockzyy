import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
from datetime import date

# Set Streamlit page config
st.set_page_config(page_title="📈 Stock Forecast App", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.page_link("1_🏠_Homepage.py", label="Stock Information")
st.sidebar.page_link("pages/2_📈_prediction.py", label="Stock Prediction")

st.title("📈 Stock Price Prediction")

# --- Load Ticker Data ---
@st.cache_data
def load_ticker_data():
    try:
        return pd.read_csv("tickers.csv",on_bad_lines='skip')
    except FileNotFoundError:
        st.error("The 'tickers.csv' file was not found. Please add it to your repository.")
        return None

tickers_df = load_ticker_data()

if tickers_df is not None:
    # --- Company and Date Selection in Sidebar ---
    st.sidebar.header("Prediction Settings")
    
    company_name = st.sidebar.selectbox(
        "Search for a company",
        tickers_df["Name"]
    )
    
    start_date = st.sidebar.date_input("Select start date", date(2023, 1, 1))
    end_date = date.today()
    period = st.sidebar.slider("Days to forecast into the future", 1, 365, 90)

    # Get the corresponding ticker symbol
    ticker_symbol = tickers_df[tickers_df["Name"] == company_name]["Ticker"].iloc[0]

    # --- Load Stock Data ---
    data_load_state = st.text(f"Loading data for {company_name}...")
    
    @st.cache_data
    def load_data(ticker, start, end):
        data = yf.download(ticker, start, end)
        data.reset_index(inplace=True)
        return data

    data = load_data(ticker_symbol, start_date, end_date)
    data_load_state.text(f"Loading data for {company_name}... Done!")

    if not data.empty:
        # Display Raw Data
        st.subheader("Raw Stock Data")
        st.write(data.tail())

        # Plot Raw Data
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock Open'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Close'))
            fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
        plot_raw_data()

        # Forecasting
        st.subheader("Future Price Forecast")
        df_train = pd.DataFrame({
            'ds': pd.to_datetime(data['Date']),
            'y': pd.to_numeric(data['Close'].squeeze())
        })

        try:
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)

            st.write("#### Forecast Chart")
            fig1 = plot_plotly(m, forecast)
            st.plotly_chart(fig1)

            st.write("#### Forecast Components")
            fig2 = m.plot_components(forecast)
            st.write(fig2)

        except Exception as e:
            st.error(f"An error occurred during forecasting: {e}")

    else:
        st.warning("No data found for the selected stock and date range.")