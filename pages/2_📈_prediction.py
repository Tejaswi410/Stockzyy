import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot  import plot_plotly
from plotly import graph_objs as go

START = "2023-1-01"
END = "2023-9-20"

st.title("Prediction 📈")

stocks = ("AAPL", "MSFT", "TSLA" , "TCS.BO")
selected_stock = st.selectbox("Select dataset for prediction",stocks)

n_months = st.slider("select months of prediction ",1,4)
period  = n_months * 30

@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker,START,END)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data ....")
data = load_data(selected_stock)
data_load_state.text("Loading data.....done!")

st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text = "Time Series Data" , xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw_data()

#forecasting or predicting
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds","Close":"y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader("Predicted data")
st.write(forecast.tail())


st.write('Predict data')
fig1 = plot_plotly(m,forecast)
st.plotly_chart(fig1)

st.write('Predicted components')
fig2 = m.plot_components(forecast)
st.write(fig2)

