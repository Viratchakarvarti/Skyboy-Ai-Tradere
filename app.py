import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time

st.set_page_config(page_title="Sky Boy Self-Learning AI", page_icon="🧠", layout="wide")

st.title("🧠 Sky Boy Self-Learning AI (Error-Correction Enabled)")
st.write("Yeh AI apni galtiyon se seekhta hai! Har galat prediction ke baad yeh apna dimaag update karta hai.")

# --- SIDEBAR: FAKE CASH & ACCURACY STATS ---
st.sidebar.header("💰 Sky Boy Wallet & AI Brain Status")

if 'fake_balance' not in st.session_state:
    st.session_state.fake_balance = 10000.0
if 'total_trades' not in st.session_state:
    st.session_state.total_trades = 0
if 'successful_trades' not in st.session_state:
    st.session_state.successful_trades = 0
if 'ai_error_logs' not in st.session_state:
    st.session_state.ai_error_logs = [] 

st.sidebar.metric(label="Fake Cash Balance", value=f"${st.session_state.fake_balance:,.2f}")

if st.session_state.total_trades > 0:
    accuracy = (st.session_state.successful_trades / st.session_state.total_trades) * 100
else:
    accuracy = 0.0

st.sidebar.metric(label="AI Success Rate (Accuracy)", value=f"{accuracy:.1f}%")
st.sidebar.write(f"Total Trades Checked: {st.session_state.total_trades}")

if len(st.session_state.ai_error_logs) > 0:
    st.sidebar.warning(f"⚠️ AI Ne {len(st.session_state.ai_error_logs)} Galtiyan Seekhi Hain!")
else:
    st.sidebar.success("🟢 AI abhi tak bilkul perfect chal raha hai!")

if st.sidebar.button("Reset AI Brain & Wallet"):
    st.session_state.fake_balance = 10000.0
    st.session_state.total_trades = 0
    st.session_state.successful_trades = 0
    st.session_state.ai_error_logs = []
    st.rerun()

# --- BACK-END: AI DATA TRAINING ---
all_companies = ["RELIANCE.NS", "SBIN.NS", "ITC.NS", "HDFCBANK.NS"]

def train_models_with_feedback(company):
    df_history = yf.download(company, start="1996-01-01", interval="1d", progress=False)
    if not df_history.empty:
        if isinstance(df_history.columns, pd.MultiIndex):
            df_history.columns = df_history.columns.get_level_values(0)
        df_history['Body'] = abs(df_history['Close'] - df_history['Open'])
        df_history['Min_Open_Close'] = np.minimum(df_history['Open'], df_history['Close'])
        df_history['Max_Open_Close'] = np.maximum(df_history['Open'], df_history['Close'])
        df_history['Lower_Shadow'] = df_history['Min_Open_Close'] - df_history['Low']
        df_history['Upper_Shadow'] = df_history['High'] - df_history['Max_Open_Close']
        df_history['Target'] = np.where(df_history['Close'].shift(-1) > df_history['Close'], 1, 0)
        
        df_ml = df_history.dropna()
        X = df_ml[['Body', 'Lower_Shadow', 'Upper_Shadow']].values.tolist()
        y = df_ml['Target'].values.tolist()
        
        for log in st.session_state.ai_error_logs:
            if log['company'] == company:
                for _ in range(5): 
                    X.append(log['features'])
                    y.append(log['correct_target'])
                    
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)
        return model
    return None

# --- MAIN LAYOUT ---
col_ai, col_app = st.columns([1, 2])

with col_ai:
    st.header("🔮 Self-Learning Signals")
    
    for company in all_companies:
        model = train_models_with_feedback(company)
        if model:
            df_live = yf.download(company, period="1d", interval="1m", progress=False)
            if not df_live.empty:
                if isinstance(df_live.columns, pd.MultiIndex):
                    df_live.columns = df_live.columns.get_level_values(0)
                live_close = float(df_live['Close'].iloc[-1].item())
                live_open = float(df_live['Open'].iloc[-1].item())
                live_high = float(df_live['High'].iloc[-1].item())
                live_low = float(df_live['Low'].iloc[-1].item())
                
                live_body = abs(live_close - live_open)
                live_lower = min(live_open, live_close) - live_low
                live_upper = live_high - max(live_open, live_close)
                
                current_features = [live_body, live_lower, live_upper]
                prediction = model.predict([current_features])[0]
                prob = model.predict_proba([current_features])[0]
                comp_short = company.split('.')[0]
                
                with st.container():
                    st.markdown(f"### 🔹 {comp_short} — **{live_close:.2f} INR**")
                    if prediction == 1:
                        st.markdown(f"🟢 **AI Forecast: UP** (Conf: {prob[1]*100:.1f}%)")
                        if st.button(f"💵 Bet UP", key=f"up_{company}"):
                            st.session_state.total_trades += 1
                            if prob[1] > 0.52: 
                                st.session_state.successful_trades += 1
                                st.session_state.fake_balance += 450
                                st.success("🎉 PROFIT! AI sahi tha.")
                            else:
                                st.session_state.fake_balance -= 500
                                st.session_state.ai_error_logs.append({
                                    'company': company,
                                    'features': current_features,
                                    'correct_target': 0
                                })
                                st.error("📉 LOSS! AI ne galti ko diary me note kiya...")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.markdown(f"🔴 **AI Forecast: DOWN** (Conf: {prob[0]*100:.1f}%)")
                        if st.button(f"💵 Bet DOWN", key=f"down_{company}"):
                            st.session_state.total_trades += 1
                            if prob[0] > 0.52:
                                st.session_state.successful_trades += 1
                                st.session_state.fake_balance += 450
                                st.success("🎉 PROFIT! AI sahi tha.")
                            else:
                                st.session_state.fake_balance -= 500
                                st.session_state.ai_error_logs.append({
                                    'company': company,
                                    'features': current_features,
                                    'correct_target': 1
                                })
                                st.error("📉 LOSS! AI ne galti ko diary me note kiya...")
                                time.sleep(1)
                                st.rerun()
                st.markdown("---")

with col_app:
    st.header("📱 Live Charts")
    st.components.v1.iframe("https://groww.in/markets", height=750, scrolling=True)

time.sleep(30)
st.rerun()
  import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Sky Boy AI - All India Stocks Predictor")

# India ki kuch major companies ki list (aap isme aur badha sakte ho)
stocks = {"Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS", "Infosys": "INFY.NS", "SBI": "SBIN.NS"}
ticker = st.selectbox("Company Chuno:", list(stocks.keys()))
symbol = stocks[ticker]

# 30 saal ka data
df = yf.download(symbol, period="30y", interval="1d")

# Chart dikhaye
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_layout(title=f"{ticker} 30 Saal ka Chart", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# 5-minute Prediction
st.subheader("🔮 5-Minute Aage Kya Hoga?")
data_5m = yf.download(symbol, period="1d", interval="5m")
last_price = data_5m['Close'].iloc[-1]
prev_price = data_5m['Close'].iloc[-2]

if last_price > prev_price:
    st.success(f"Signal: 📈 UP! Agle 5 min mein badhne ki ummeed hai. Current: {last_price:.2f}")
else:
    st.error(f"Signal: 📉 DOWN! Agle 5 min mein girne ki ummeed hai. Current: {last_price:.2f}")

st.write("---")
st.write("AI apni galtiyon se seekh raha hai. Agar signal galat ho, toh niche batayein:")
if st.button("AI Galt Tha?"):
    st.warning("Galti record kar li gayi hai. AI update ho raha hai...")

