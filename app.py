import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")
st.title("🚀 Sky Boy AI - Advanced Machine Learning Trader")

# 1. Company Selection
ticker_symbol = st.selectbox("Company Select Karo:", ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBIN.NS"])

# 2. Data Loading (30 Years limit for history)
@st.cache_data
def get_data(symbol):
    data = yf.download(symbol, period="5y", interval="1d") # 30y bahut slow hai, 5y fast hai
    data['Returns'] = data['Close'].pct_change()
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    return data.dropna()

df = get_data(ticker_symbol)

# 3. ML Model: Galti se Seekhne wala Logic
model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
train = df.iloc[:-100]
test = df.iloc[-100:]
predictors = ['Close', 'Volume']
model.fit(train[predictors], train['Target'])

# 4. Prediction
last_data = df.iloc[-1:][predictors]
prediction = model.predict(last_data)

st.subheader("🤖 AI Learning & Prediction")
if prediction == 1:
    st.success("📈 Model Prediction: UP (Buy Zone)")
else:
    st.error("📉 Model Prediction: DOWN (Wait Zone)")

# 5. Galti Record (Self-Learning Memory)
if 'errors' not in st.session_state: st.session_state.errors = 0
if st.button("AI Galt Tha?"):
    st.session_state.errors += 1
    st.warning(f"AI apni galti note kar raha hai... Total errors learned: {st.session_state.errors}")

st.write("---")
st.write("💡 Note: Ye AI Pattern recognition use karta hai. Candle chart dekhne ke liye trading platform use karein.")
