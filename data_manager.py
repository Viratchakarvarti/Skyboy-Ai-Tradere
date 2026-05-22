import yfinance as yf
def get_stock_data(symbol):
    return yf.download(symbol, period="5d", interval="5m")
  
