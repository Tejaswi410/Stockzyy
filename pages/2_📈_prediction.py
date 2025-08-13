import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from prophet.diagnostics import cross_validation, performance_metrics
from plotly import graph_objs as go
import pandas as pd
from datetime import date

# Set Streamlit page config
st.set_page_config(page_title="📈 Stock Forecast App", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.page_link("1_🏠_Homepage.py",label = "Stock Information")
st.sidebar.page_link("pages/2_📈_prediction.py", label = "Stock Prediction")

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

    data['Date'] = pd.to_datetime(data['Date']).dt.date


    if not data.empty:
        # Display Raw Data
        st.subheader("Raw Stock Data")
        st.write(f"Showing data for {company_name} from {start_date} to {end_date}")
        st.write(data.head())
        st.write(data.tail())
        
        st.divider()

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

            # Forecast Chart Section
            with st.container():
                st.write("#### 📈 Forecast Chart")
                fig1 = plot_plotly(m, forecast)
                st.plotly_chart(fig1, use_container_width=True)
            
            # Add visual separator
            st.divider()
            
            # Components Section
            with st.container():
                st.write("#### 🔄 Forecast Components")
                fig2 = m.plot_components(forecast)
                st.write(fig2)
            
            # Add another visual separator
            st.divider()
            
            # Performance Metrics Section
            with st.container():
                st.write("#### 📊 Model Performance")
                st.info("💡 These metrics show how well the model performs on historical data")
                
                # Create columns for better layout
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Performance metrics
                    df_cv = cross_validation(m, initial='365 days', period='90 days', horizon='90 days', parallel="threads")
                    df_p = performance_metrics(df_cv)
                    st.dataframe(df_p, use_container_width=True)
                
                with col2:
                    st.write("**Metric Explanations:**")
                    st.write("• **MAE**: Mean Absolute Error")
                    st.write("• **MSE**: Mean Squared Error")
                    st.write("• **RMSE**: Root Mean Squared Error")
                    st.write("• **MAPE**: Mean Absolute Percentage Error")

        except Exception as e:
            st.error(f"An error occurred during forecasting: {e}")
    else:
        st.warning("No data found for the selected stock and date range.")