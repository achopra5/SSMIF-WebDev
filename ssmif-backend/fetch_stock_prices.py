import pandas as pd
import yfinance as yf
from clickhouse_driver import Client

# Connect to ClickHouse
client = Client(host="localhost", database="ssmif", user="adichop", password="Aditya1803*")

# Get unique tickers from holdings
query = "SELECT DISTINCT Symbol FROM holdings"
tickers = [row[0] for row in client.execute(query)]

# Exclude invalid tickers (currencies, delisted stocks)
invalid_tickers = {"JPY", "EUR", "GBP"}
ticker_mapping = {"FB": "META"}  # Replace FB with META

# Apply ticker corrections
valid_tickers = [ticker_mapping.get(t, t) for t in tickers if t not in invalid_tickers]

# Predefined list of ETFs in the holdings dataset
ETF_LIST = {"QQQ", "SPY", "XLF", "XLV", "VUG"}  # Add more if needed

# Identify ETFs in holdings
etfs_in_holdings = [t for t in valid_tickers if t in ETF_LIST]

# Ensure `etf_sector_breakdown` table exists
client.execute("""
CREATE TABLE IF NOT EXISTS etf_sector_breakdown (
    ETF String,
    Stock String,
    Weight Float32
) ENGINE = MergeTree()
ORDER BY ETF;
""")

# Function to fetch ETF holdings from Yahoo Finance
def fetch_etf_holdings(etf_ticker):
    try:
        etf = yf.Ticker(etf_ticker)
        holdings = etf.info.get("holdings", None)  

        if not holdings:
            print(f"No holdings data found for {etf_ticker}")
            return None

        # Convert holdings to a DataFrame
        holdings_df = pd.DataFrame(holdings, columns=["symbol", "holdingPercent"])
        return holdings_df

    except Exception as e:
        print(f"Error fetching ETF holdings for {etf_ticker}: {e}")
        return None

# Function to store ETF sector breakdown while avoiding duplicates
def store_etf_sector_breakdown(etf_ticker, holdings_df):
    if holdings_df is None:
        return

    # Check for existing ETF sector data
    existing_stocks_query = f"SELECT DISTINCT Stock FROM etf_sector_breakdown WHERE ETF = '{etf_ticker}'"
    existing_stocks = {row[0] for row in client.execute(existing_stocks_query)}

    # Insert only new records
    records = [
        (etf_ticker, row["symbol"], float(row["holdingPercent"]))
        for _, row in holdings_df.iterrows()
        if row["symbol"] not in existing_stocks
    ]

    if records:
        client.execute(
            "INSERT INTO etf_sector_breakdown (ETF, Stock, Weight) VALUES",
            records
        )
        print(f" ETF sector breakdown for {etf_ticker} stored successfully!")
    else:
        print(f"No new ETF data to insert for {etf_ticker}")

# Process each ETF in the holdings
for etf in etfs_in_holdings:
    print(f" Processing {etf} ETF breakdown...")
    etf_holdings = fetch_etf_holdings(etf)
    store_etf_sector_breakdown(etf, etf_holdings)

# Fetch and store stock prices
def fetch_stock_prices(symbol, start="2015-01-01", end="2025-01-01"):
    print(f"Fetching data for {symbol}...")
    data = yf.download(symbol, start=start, end=end)

    if data.empty:
        print(f" No data found for {symbol}")
        return

    data["Volume"] = data["Volume"].fillna(0).astype(int)
    print(f"Latest available data for {symbol}: {data.index[-1].date()}")

    existing_dates_query = f"SELECT DISTINCT Date FROM stock_prices WHERE Symbol = '{symbol}'"
    existing_dates = {row[0] for row in client.execute(existing_dates_query)}

    records = [
        (
            date.date(), symbol,
            float(row["Open"]), float(row["High"]),
            float(row["Low"]), float(row["Close"]),
            int(row["Volume"])
        )
        for date, row in data.iterrows() if date.date() not in existing_dates
    ]

    if records:
        client.execute(
            "INSERT INTO stock_prices (Date, Symbol, Open, High, Low, Close, Volume) VALUES",
            records
        )
        print(f" Data for {symbol} inserted successfully!")
    else:
        print(f" No new data to insert for {symbol}")

# Fetch prices for all tickers
for ticker in valid_tickers:
    fetch_stock_prices(ticker)

print(" Stock prices and ETF sector breakdown loaded successfully!")
