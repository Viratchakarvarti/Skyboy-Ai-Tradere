import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def get_data(symbol):
    try:
        # Pura data ek baar mein fetch karne ki jagah 'yf.Ticker' object use karenge
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1mo", interval="5m")
        return df
    except Exception as e:
        return None
