import yfinance as yf
import streamlit as st

@st.cache_data(ttl=3600)
def get_data(symbol):
    return yf.download(symbol, period="15y", interval="5m")
