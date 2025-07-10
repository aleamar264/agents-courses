# filename: fetch_stock_data.py

import yfinance as yf

def fetch_stock_data(tickers):
    stocks = yf.download(tickers, period="1mo")
    print(stocks)

if __name__ == "__main__":
    tickers = ["GOOGL", "AAPL"]  # Replace with your desired stock tickers
    fetch_stock_data(tickers)