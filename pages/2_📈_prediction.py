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
st.sidebar.page_link("1_🏠_Homepage.py", label="Homepage")
st.sidebar.page_link("pages/2_📈_prediction.py", label="Stock Prediction")

# Title
st.title("📈 Stock Price Prediction")

# --- Stock Selection ---
stocks = ("AAPL", "MSFT", "TSLA", "GOOG", "AMZN", "TCS.BO")
selected_stock = st.selectbox("Select a stock for prediction", stocks)

# --- Date Selection ---
start_date = st.date_input("Select start date for prediction", date(2023, 1, 1))
end_date = date.today() # Predict up to the current date

# --- Load Stock Data ---
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text(f"Loading data for {selected_stock}...")
data = load_data(selected_stock, start_date, end_date)
data_load_state.text(f"Loading data for {selected_stock}...done!")

# --- Display Raw Data ---
st.subheader("Raw Stock Data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# --- Forecasting ---
if not data.empty:
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

    # Calculate prediction period
    n_days = (end_date - start_date).days
    period = st.slider("Select number of days for prediction", 1, 365, 90)

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # --- Display Predicted Data ---
    st.subheader("Predicted Data")
    st.write(forecast.tail())

    st.write('### Prediction Chart')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("### Prediction Components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
else:
    st.warning("No data to display. Please select a valid date range.")