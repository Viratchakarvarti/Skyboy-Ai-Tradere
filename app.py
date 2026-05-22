import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st.title("🚀 Sky Boy AI - Live Pro Trader")

# Auto-refresh har 10 seconds mein (Live feel ke liye)
st_autorefresh(interval=10000, key="datarefresh")

stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS"}
ticker = st.selectbox("Company:", list(stocks.keys()))
symbol = stocks[ticker]

# Data Fetching
df = yf.download(symbol, period="5d", interval="5m")

if not df.empty:
    # 1. Digital Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title=f"Live Chart: {ticker}", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # 2. Prediction (Simple Logic)
    last_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    signal = "UP" if last_price > prev_price else "DOWN"
    
    st.subheader(f"🤖 AI Signal: {signal}")
    
    # 3. Accuracy Tracker (Galti se seekhna)
    if 'wins' not in st.session_state: st.session_state.wins = 0
    if 'losses' not in st.session_state: st.session_state.losses = 0
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("AI Sahi Tha"):
            st.session_state.wins += 1
    with col2:
        if st.button("AI Galt Tha"):
            st.session_state.losses += 1
            
    st.write(f"📊 Accuracy: Sahi: {st.session_state.wins} | Galt: {st.session_state.losses}")
    
    # 4. Candlestick Patterns explain (Learning)
    st.write("---")
    st.info("💡 Pro Tip: Green candle = Buyers, Red candle = Sellers.")
else:
    st.warning("Data load ho raha hai...")
