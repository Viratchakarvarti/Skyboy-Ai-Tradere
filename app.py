import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - Pro Trader Dashboard")

stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker = st.selectbox("Company Select Karo:", list(stocks.keys()))
symbol = stocks[ticker]

# Chart ke liye data
df = yf.download(symbol, period="30y", interval="1d")

if not df.empty:
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title=f"{ticker} - 30 Saal ka Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # Prediction
    st.subheader("🔮 Agle 5 Minute Ka Signal")
    data_5m = yf.download(symbol, period="1d", interval="5m")
    
    if len(data_5m) >= 2:
        # Yahan humne .item() ka use kiya hai jo error khatam kar dega
        last_price = float(data_5m['Close'].iloc[-1].item())
        prev_price = float(data_5m['Close'].iloc[-2].item())
        diff = last_price - prev_price
        
        if diff > 0:
            st.success(f"📈 Signal: UP | Change: +{diff:.2f}")
        else:
            st.error(f"📉 Signal: DOWN | Change: {diff:.2f}")
    else:
        st.write("Data update ho raha hai, please wait...")
        
