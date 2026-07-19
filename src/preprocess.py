############ To do ######################################################################

############ Notes ######################################################################
# Raw Data - (data/raw/stock_prices.csv)
#         ↓
# Preprocessing - (src/preprocess.py)
#         ↓
# Clean Dataset - (data/processed/stock_prices_clean.csv)
#         ↓
# Factor Calculation - (notebooks/02_factor_calculation.ipynb)
#         ↓
# Momentum - Volatility - Trend
#         ↓
# Stock Ranking Model

from pathlib import Path
import pandas as pd 

############### Data Processing ####################################################################

#define the path to the raw data 
dataPath = Path("data/raw/stock_prices.csv")

# load the csv without headers
loadStock = pd.read_csv(dataPath, header=None)

# First row contains the column names (Close, Volume, etc.)- Second row contains ticker names - Third row is useless -  Data starts from row 3

# Create clean column names
columns = loadStock.iloc[0] + "_" + loadStock.iloc[1]

# Assign column names
loadStock.columns = columns

# Remove the first 3 rows
loadStock = loadStock.iloc[3:].reset_index(drop=True)

# Rename first column to Date
loadStock.rename(
    columns={loadStock.columns[0]: "Date"},
    inplace=True
)

# Convert Date
loadStock["Date"] = pd.to_datetime(loadStock["Date"])

# Convert stock data columns from strings to numbers
for col in loadStock.columns[1:]:
    loadStock[col] = pd.to_numeric(loadStock[col], errors="coerce")

#Print results
print(loadStock.head())
print(loadStock.info())
print(loadStock.dtypes.head())
print(loadStock.isnull().sum().sum())
print(loadStock["Date"].duplicated().sum())

#write to the file - Overwrites the file completely
newPath = Path("data/processed/stock_prices_clean.csv")

loadStock.to_csv(
    newPath,
    index=False
)
############### Factor Calculation ####################################################################
#Loas clean stock price datatset into a DataFram and treat "Date" column as actual dates
#DataFrame is an Excel spreadsheet inside python
#parse_dates, without it pandas might read dates as string 
#CSV
# Date          Close_AAPL   Close_AMZN
# 2015-01-02    24.19        15.42
# 2015-01-05    23.51        15.10

#Dataframe
#         Date        Close_AAPL   Close_AMZN
# 0   2015-01-02       24.19        15.42
# 1   2015-01-05       23.51        15.10

df = pd.read_csv(
    "data/processed/stock_prices_clean.csv",
    parse_dates=["Date"]
)

#Calculate daily returns