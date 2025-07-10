# filename: plot_stocks.py

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download stock data for META and TESLA
tickers = ["META", "TSLA"]
data = yf.download(tickers, period="max")

# Plot the closing prices
plt.figure(figsize=(10, 6))
plt.plot(data['Close']['META'], label='META (Facebook)')
plt.plot(data['Close']['TSLA'], label='TSLA (Tesla)')
plt.title('Stock Price Comparison: META and TESLA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()