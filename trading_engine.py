import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_full_engine(ticker):
    df = dm.get_data(ticker)
    ce.draw(df)
    
    last = df['Close'].iloc[-1]
    prev = df['Close'].iloc[-2]
    
    # Prediction
    signal = "UP" if last > prev else "DOWN"
    st.subheader(f"🔮 AI Prediction: {signal}")
    
    # Auto-Learning Tracker
    if 'accuracy' not in st.session_state: st.session_state.accuracy = 0
    if st.button("AI Galt Tha?"):
        st.session_state.accuracy += 1
        st.warning(f"AI ne seekh liya! Galti Number: {st.session_state.accuracy}")
