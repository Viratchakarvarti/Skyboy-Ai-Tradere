import plotly.graph_objects as go
import streamlit as st

def draw(df):
    fig = go.Figure(data=[go.Candlestick(x=df.index[-100:], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title="Live Candlestick Chart", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
