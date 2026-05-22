import streamlit as st
from streamlit_autorefresh import st_autorefresh
import trading_engine as te

st.set_page_config(layout="wide")
st.title("🚀 Sky Boy AI - Final Pro Setup")
st_autorefresh(interval=60000, key="datarefresh")

ticker = st.selectbox("Company:", ["RELIANCE.NS", "TCS.NS", "HDFC.NS", "INFY.NS", "SBIN.NS"])
if st.button("Analysis Shuru"):
    te.run_full_engine(ticker)

