import data_manager as dm
import chart_engine as ce
import streamlit as st

def run_full_engine(ticker):
    # Data fetch karo
    df = dm.get_data(ticker)
    
    # Check: Agar data bilkul nahi mila
    if df is None or df.empty:
        st.error("Market data server se nahi mil raha. Ho sakta hai market closed ho ya connection slow ho.")
        return
        
    # Chart draw karo
    ce.draw(df)
    
    # Prediction: Sirf tabhi calculation karo jab data mein rows ho
    if len(df) >= 2:
        try:
            # .iloc[-1] se aakhri row nikal rahe hain
            last = float(df['Close'].iloc[-1])
            prev = float(df['Close'].iloc[-2])
            
            signal = "UP" if last > prev else "DOWN"
            st.subheader(f"🔮 AI Prediction: {signal}")
        except Exception:
            st.write("Data format mein dikkat hai, market closed hone ki wajah se.")
    else:
        st.warning("Data kam hai, abhi prediction nahi kar sakte.")
