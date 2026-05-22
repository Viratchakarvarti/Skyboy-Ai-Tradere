import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_full_engine(ticker):
    df = dm.get_data(ticker)
    
    # Isse pata chalega ki asli dikkat kya hai
    if df is None or df.empty:
        st.error(f"Server se {ticker} ka data nahi aa raha. (Internet ya Yfinance API issue)")
        return
        
    ce.draw(df)
    
    # Yahan .iloc[-1] ke saath check lagaya hai
    try:
        last = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2])
        signal = "UP" if last > prev else "DOWN"
        st.subheader(f"🔮 AI Prediction: {signal}")
    except Exception as e:
        st.warning("Data calculate nahi ho pa raha, market abhi shayad closed hai.")
