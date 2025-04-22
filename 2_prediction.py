import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title="📈 Stock Forecast App", layout="wide")

# Title
st.title("📈 Stock Price Prediction ")

# Constants
DEFAULT_START = "2023-01-01"
DEFAULT_END = "2023-12-31"

@st.cache_data
def load_ticker_list():
    return pd.read_csv("tickers.csv")

tickers_df = load_ticker_list()

# Sidebar dropdown: Searchable stock list from tickers.csv
selected_row = st.sidebar.selectbox(
    "🔍 Search and select a stock",
    tickers_df.apply(lambda row: f"{row['Name']} ({row['Ticker']})", axis=1)
)

# Extract just the ticker symbol (e.g., "AAPL" from "Apple Inc. (AAPL)")
selected_stock = selected_row.split("(")[-1].strip(")")


n_months = st.sidebar.slider("Months to forecast", 1, 4)
period = n_months * 30  # Prophet works in days

start_date = st.sidebar.date_input("Start Date", pd.to_datetime(DEFAULT_START))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(DEFAULT_END))

# Load stock data
@st.cache_data
def load_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)
    return df

st.info(f"Fetching data for **{selected_stock}**...")
data = load_stock_data(selected_stock, start_date, end_date)

if data.empty:
    st.error("No data found for the selected date range.")
    st.stop()

# Show raw data
st.subheader("📊 Raw Stock Data")
st.write(data.tail())

# Plot raw open/close price
def plot_time_series(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name='Open'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'))
    fig.update_layout(title="Stock Price History", xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

plot_time_series(data)

# Prepare data for Prophet
if "Date" not in data.columns or "Close" not in data.columns:
    st.error("Data does not contain required 'Date' and 'Close' columns.")
    st.stop()

# Ensure correct structure
df_train = data[['Date', 'Close']].copy()
df_train.columns = ['ds', 'y']  # Rename for Prophet

# Sanity check: Print column types
st.write("Column data types:", df_train.dtypes)

# Ensure 'y' is numeric and clean
if not pd.api.types.is_numeric_dtype(df_train['y']):
    try:
        df_train['y'] = pd.to_numeric(df_train['y'], errors='coerce')
    except Exception as e:
        st.error(f"Conversion to numeric failed: {e}")
        st.stop()

# Drop rows with NaN
df_train.dropna(subset=['y'], inplace=True)

# Final check: valid format
if df_train.empty or df_train['y'].ndim != 1:
    st.error("Cleaned training data is empty or malformed.")
    st.stop()


# Forecasting
st.subheader("📈 Forecasting Future Prices")


try:
    model = Prophet(daily_seasonality=True)
    model.fit(df_train)  # Data is already cleaned above
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

    # Show forecast table
    st.subheader("🔮 Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    # Forecast Plot (interactive)
    st.subheader("📉 Forecast Chart")
    fig_forecast = plot_plotly(model, forecast)
    st.plotly_chart(fig_forecast, use_container_width=True)

    # Forecast Components
    st.subheader("🔍 Forecast Components (Trend, Weekly, Yearly)")
    fig_components = model.plot_components(forecast)
    st.pyplot(fig_components)

except Exception as e:
    st.error(f"Forecasting failed: {e}")

