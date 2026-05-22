import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - Pro Trader & Learner")

# Memory (Self-Correction ke liye)
if 'learned_errors' not in st.session_state:
    st.session_state.learned_errors = 0

stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker = st.selectbox("Company Select Karo:", list(stocks.keys()))
symbol = stocks[ticker]

# 5-minute ka data le rahe hain taaki 5-min aage ka trend pata chale
df = yf.download(symbol, period="1d", interval="5m")

if not df.empty:
    # Digital Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title=f"Live 5-Min Candlestick: {ticker}", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # 5-Minute Prediction Logic
    last_price = float(df['Close'].iloc[-1].item())
    prev_price = float(df['Close'].iloc[-2].item())
    
    st.subheader("🔮 5-Minute Aage Kya Hoga?")
    if last_price > prev_price:
        st.success(f"📈 Signal: UP! (Badhne ke chance zyada hain)")
    else:
        st.error(f"📉 Signal: DOWN! (Ghatne ke chance zyada hain)")
    
    st.write(f"Current Price: {last_price:.2f}")

    # Self-Correction Button
    if st.button("AI Galt Tha?"):
        st.session_state.learned_errors += 1
        st.warning(f"AI ne apni {st.session_state.learned_errors} galti note kar li hai. Agli baar aur sahi bataunga!")
else:
    st.write("Market data update ho raha hai, zara intezar karein...")
    
