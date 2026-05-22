import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - All India Stocks Predictor")

stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker_name = st.selectbox("Company Chuno:", list(stocks.keys()))
symbol = stocks[ticker_name]

df = yf.download(symbol, period="30y", interval="1d")

fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_layout(title=f"{ticker_name} - 30 Saal ka Historical Chart", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔮 5-Minute Aage Kya Hoga?")
data_5m = yf.download(symbol, period="1d", interval="5m")

if len(data_5m) > 1:
    last_price = data_5m['Close'].iloc[-1]
    prev_price = data_5m['Close'].iloc[-2]

    if last_price > prev_price:
        st.success(f"Signal: 📈 UP! Current: {last_price:.2f}")
    else:
        st.error(f"Signal: 📉 DOWN! Current: {last_price:.2f}")

st.write("---")
if st.button("AI Galt Tha?"):
    st.warning("Galti record kar li gayi hai. AI update ho raha hai...")
