import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - Pro Trader Dashboard")

# 1-minute auto-refresh
st.empty()
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker = st.selectbox("Company Select Karo:", list(stocks.keys()))
symbol = stocks[ticker]

# 30 Saal ka data
df = yf.download(symbol, period="30y", interval="1d")

# Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_layout(title=f"{ticker} - Analysis", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# 5-Minute Forecast
st.subheader("🔮 Agle 5 Minute Ka Signal")
data_5m = yf.download(symbol, period="1d", interval="5m")
if len(data_5m) > 1:
    diff = data_5m['Close'].iloc[-1] - data_5m['Close'].iloc[-2]
    target = data_5m['Close'].iloc[-1] + diff
    
    if diff > 0:
        st.success(f"📈 Signal: UP | Target Price: {target:.2f}")
    else:
        st.error(f"📉 Signal: DOWN | Target Price: {target:.2f}")

# Auto-refresh
time.sleep(60)
st.rerun()
