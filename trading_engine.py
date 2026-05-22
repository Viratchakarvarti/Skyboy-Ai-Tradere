import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_full_engine(ticker):
    df = dm.get_data(ticker)
    
    # SIRF YE CHECK BADLA HAI - Ye galti pakad lega
    if df is not None and not df.empty and len(df) > 1:
        ce.draw(df)
        
        last = df['Close'].iloc[-1]
        prev = df['Close'].iloc[-2]
        
        signal = "UP" if last > prev else "DOWN"
        st.subheader(f"🔮 AI Prediction: {signal}")
        
        if 'accuracy' not in st.session_state: st.session_state.accuracy = 0
        if st.button("AI Galt Tha?"):
            st.session_state.accuracy += 1
            st.warning(f"Galti note ho gayi. Galti Number: {st.session_state.accuracy}")
    else:
        st.error("Data load ho raha hai, zara ruk jao Aakash bhai...")
