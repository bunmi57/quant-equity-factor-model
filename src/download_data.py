import yfinance as yf
from config import stocks

data = yf.download(
    stocks,
    start="2015-01-01",
    auto_adjust=True,
    progress=False
)

# print(data)
# print(data.head())

#save raw data 
data.to_csv("../data/raw/stock_prices.csv")
print("Data downloaded successfully!")