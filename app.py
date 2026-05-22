import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - Pro Trader Dashboard")

# Stock Selection
stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker = st.selectbox("Company Select Karo:", list(stocks.keys()))
symbol = stocks[ticker]

# 30 Saal ka data (Safe Fetch)
df = yf.download(symbol, period="30y", interval="1d")

if not df.empty:
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title=f"{ticker} - Historical Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # 5-Minute Forecast with Error Handling
    st.subheader("🔮 Agle 5 Minute Ka Signal")
    data_5m = yf.download(symbol, period="1d", interval="5m")
    
    if len(data_5m) >= 2:
        # Data mil gaya, ab calculation karo
        last_price = float(data_5m['Close'].iloc[-1])
        prev_price = float(data_5m['Close'].iloc[-2])
        diff = last_price - prev_price
        
        if diff > 0:
            st.success(f"📈 Signal: UP | Price Change: +{diff:.2f}")
        else:
            st.error(f"📉 Signal: DOWN | Price Change: {diff:.2f}")
    else:
        st.warning("Data fetch ho raha hai, please wait...")
else:
    st.error("Market data load nahi ho pa raha, shayad internet ya API mein issue hai.")
    
