import streamlit as st
import yfinance as fn

st.title("Stocks prediction AI ")

def get_ticker(name):
    company = fn.Ticker(name)
    return company

c1 = get_ticker("AAPL")
c2 = get_ticker("MSFT")
c3 = get_ticker("TSLA")
c4 = get_ticker("TCS.BO")

apple = fn.download("AAPL", start = "2023-7-20", end = "2023-9-20")
microsoft = fn.download("MSFT", start = "2023-7-20", end = "2023-9-20")
tesla = fn.download("TSLA", start = "2023-7-20", end = "2023-9-20")
tcs =  fn.download("TCS.BO", start = "2023-7-20", end = "2023-9-20")

data1 = c1.history(period = "3mo")
data2 = c2.history(period = "3mo")
data3 = c3.history(period = "3mo")
data4 = c4.history(period = "3mo")

#for apple
st.write(""" ### Apple """)
st.write(c1.info['longBusinessSummary'])
st.write(apple)
st.line_chart(data1.values)

st.write(""" ### Microsoft """)
st.write(c2.info['longBusinessSummary'])
st.write(microsoft)
st.line_chart(data2.values)

st.write(""" ### Tesla """)
st.write(c3.info['longBusinessSummary'])
st.write(tesla)
st.line_chart(data3.values)

st.write(""" ### Tata consultancy services """)
st.write(c4.info['longBusinessSummary'])
st.write(tcs)
st.line_chart(data4.values)