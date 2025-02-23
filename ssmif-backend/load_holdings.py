import pandas as pd
from clickhouse_driver import Client

# Connect to ClickHouse
client = Client(host="localhost", database="ssmif", user="adichop", password="Aditya1803*")

# Ensure `holdings` and `non_equity_holdings` tables exist
client.execute("""
CREATE TABLE IF NOT EXISTS holdings (
    Date Date,
    Symbol String,
    Shares Float32
) ENGINE = MergeTree()
ORDER BY (Date, Symbol);
""")

client.execute("""
CREATE TABLE IF NOT EXISTS non_equity_holdings (
    Date Date,
    Asset_Type String,
    Symbol String,
    Quantity Float32,
    Value Float32
) ENGINE = MergeTree()
ORDER BY (Date, Symbol);
""")

# Load holdings CSV
holdings_df = pd.read_csv('/Users/adi/SSMIF Coding Challenge S25/Development Coding Challenge S25/holdings.csv')

# Convert 'Date' column to datetime format
holdings_df["Date"] = pd.to_datetime(holdings_df["Date"]).dt.date

# Define non-equity asset types
non_equity_assets = {"JPY", "EUR", "GBP", "BONDS", "GOLD", "OIL"}

# Separate equity and non-equity holdings
equity_holdings = holdings_df[~holdings_df["Symbol"].isin(non_equity_assets)]
non_equity_holdings = holdings_df[holdings_df["Symbol"].isin(non_equity_assets)]

# Function to insert equity holdings while avoiding duplicates
def insert_equity_holdings(equity_df):
    existing_data = client.execute("SELECT Date, Symbol FROM holdings")
    existing_records = {(row[0], row[1]) for row in existing_data}

    new_records = [
        (row["Date"], row["Symbol"], row["Shares"])
        for _, row in equity_df.iterrows()
        if (row["Date"], row["Symbol"]) not in existing_records
    ]

    if new_records:
        client.execute("INSERT INTO holdings (Date, Symbol, Shares) VALUES", new_records)
        print(f"✅ Inserted {len(new_records)} new equity holdings.")
    else:
        print("🔄 No new equity holdings to insert.")

# Function to insert non-equity holdings while avoiding duplicates
def insert_non_equity_holdings(non_equity_df):
    existing_data = client.execute("SELECT Date, Symbol FROM non_equity_holdings")
    existing_records = {(row[0], row[1]) for row in existing_data}

    new_records = [
        (row["Date"], "Currency" if row["Symbol"] in {"JPY", "EUR", "GBP"} else "Commodity", row["Symbol"], row["Shares"], 0.0)
        for _, row in non_equity_df.iterrows()
        if (row["Date"], row["Symbol"]) not in existing_records
    ]

    if new_records:
        client.execute("INSERT INTO non_equity_holdings (Date, Asset_Type, Symbol, Quantity, Value) VALUES", new_records)
        print(f" Inserted {len(new_records)} new non-equity holdings.")
    else:
        print(" No new non-equity holdings to insert.")

# Insert data while avoiding duplicates
insert_equity_holdings(equity_holdings)
insert_non_equity_holdings(non_equity_holdings)

print("🎉 Holdings data loaded successfully, duplicates avoided!")
