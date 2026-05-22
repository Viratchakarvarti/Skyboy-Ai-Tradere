import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_full_engine(ticker):
    # Data lao
    df = dm.get_data(ticker)
    
    # 1. Check karo ki data khali toh nahi
    if df is None or df.empty:
        st.error("Market se data nahi mil raha. Reliance ya TCS check karo.")
        return

    # 2. Check karo ki kam se kam 2 rows hain (Calculation ke liye)
    if len(df) < 2:
        st.warning("Data load ho raha hai, please wait...")
        return

    # 3. Agar sab sahi hai, tabhi aage badho
    ce.draw(df)
    
    # .values[0] ka use karo taaki error na aaye
    last = float(df['Close'].iloc[-1].values[0])
    prev = float(df['Close'].iloc[-2].values[0])
    
    signal = "UP" if last > prev else "DOWN"
    st.subheader(f"🔮 AI Prediction: {signal}")
    
    if st.button("AI Galt Tha?"):
        st.warning("Galti note ho gayi.")
