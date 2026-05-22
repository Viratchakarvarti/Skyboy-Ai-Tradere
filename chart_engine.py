import plotly.graph_objects as go
import streamlit as st

def draw_chart(df, ticker):
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    st.plotly_chart(fig, use_container_width=True)
