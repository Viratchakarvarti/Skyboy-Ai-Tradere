import streamlit as st
import trading_engine as te # Logic file call ki

st.set_page_config(layout="wide")
st.title("🚀 Sky Boy AI - Pro Engine")
ticker = st.selectbox("Company:", ["RELIANCE.NS", "TCS.NS", "HDFC.NS"])

if st.button("Analysis Shuru Karein"):
    te.run_analysis(ticker)
    
