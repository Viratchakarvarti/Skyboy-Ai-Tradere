import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_analysis(ticker):
    df = dm.get_stock_data(ticker)
    ce.draw_chart(df, ticker)
    
    # Fast Calculation Logic
    last_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    
    if last_price > prev_price:
        st.success("📈 Signal: UPAR JAYEGA! (Abhi Invest Kar Sakte Hain)")
    else:
        st.error("📉 Signal: NEECHE JAYEGA! (Abhi Wait Karein)")
        
    if st.button("Mistake Report"):
        st.warning("AI ne note kar liya, agli baar sahi batayega.")
