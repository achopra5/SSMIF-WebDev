from fastapi import FastAPI, HTTPException
from clickhouse_driver import Client
import numpy as np
import pandas as pd
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return
from fastapi.middleware.cors import CORSMiddleware
from pypfopt.efficient_frontier import EfficientFrontier


# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow frontend (localhost:3000) to access backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to get a new ClickHouse connection
def get_clickhouse_client():
    return Client(
        host="localhost",
        database="ssmif",
        user="adichop",
        password="Aditya1803*",  
        port=9000
    )

@app.get("/daily-returns")
def get_daily_returns():
    query = """
    SELECT Trade_Date, Daily_Return
    FROM daily_returns
    ORDER BY Trade_Date;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        return {"daily_returns": [{"date": row[0], "return": row[1]} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def calculate_sharpe_ratio():
    """
    Computes the Sharpe Ratio over time using a rolling window.
    """
    query = """
    SELECT Trade_Date, Daily_Return
    FROM daily_returns
    ORDER BY Trade_Date;
    """

    try:
        # Fetch data from ClickHouse
        client = get_clickhouse_client()
        result = client.execute(query)
        if not result:
            return []

        # Convert to DataFrame
        df = pd.DataFrame(result, columns=["date", "daily_return"])
        df["date"] = pd.to_datetime(df["date"])

        # Ensure enough data points
        if df.shape[0] < 30:
            print(" Not enough data to compute Sharpe Ratio")
            return {"error": "Not enough data points to compute Sharpe Ratio"}

        # Compute rolling Sharpe Ratio
        rolling_window = 30  # 30-day rolling window
        df["rolling_return"] = df["daily_return"].rolling(window=rolling_window).mean() * 252  # Annualized return
        df["rolling_volatility"] = df["daily_return"].rolling(window=rolling_window).std() * np.sqrt(252)  # Annualized volatility

        #  Avoid division by zero
        df["sharpe_ratio"] = np.where(df["rolling_volatility"] == 0, 0, df["rolling_return"] / df["rolling_volatility"])

        # Drop NaN values from the initial rolling window
        df.dropna(subset=["sharpe_ratio"], inplace=True)

        #  Debugging logs
        #print(f" Sharpe Ratio Computed: {df[['date', 'sharpe_ratio']].tail(5)}")

        return df[["date", "sharpe_ratio"]].to_dict(orient="records")

    except Exception as e:
        print(f"Error computing Sharpe Ratio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sharpe-ratio")
def get_sharpe_ratio():
    return {"sharpe_ratio": calculate_sharpe_ratio()}


@app.get("/optimize-portfolio")
def optimize_portfolio():
    """
    Computes the optimized portfolio weights using PyPortfolioOpt's Max Sharpe Ratio method.
    """

    query = """
    WITH stock_daily_returns AS (
    SELECT
        Symbol,
        Date,
        (Close - lagInFrame(Close, 1) OVER (PARTITION BY Symbol ORDER BY Date ASC)) /
        NULLIF(lagInFrame(Close, 1) OVER (PARTITION BY Symbol ORDER BY Date ASC), 0) AS daily_return
    FROM stock_prices
    WHERE Close IS NOT NULL
)

SELECT 
    Symbol, 
    toStartOfMonth(Date) AS Month, 
    COALESCE(AVG(daily_return), 0) AS monthly_return  -- Replace NULL with 0
FROM stock_daily_returns
WHERE isFinite(daily_return)  -- Ensure no infinite values
GROUP BY Symbol, Month
ORDER BY Month ASC, Symbol ASC;
    """

    try:
        print("🔍 Fetching stock returns...")
        client = get_clickhouse_client()
        returns_data = client.execute(query)
        df = pd.DataFrame(returns_data, columns=["Symbol", "Month", "monthly_return"])

        if df.empty:
            print(" Error: No stock return data found!")
            return {"error": "No stock return data available"}

        # Reshape data: Pivot table to make Symbols as columns
        pivot_df = df.pivot(index="Month", columns="Symbol", values="monthly_return")

        print(f"📊 Pivoted Data Shape: {pivot_df.shape}")
        print(f"🔍 Checking for NaN values: {pivot_df.isna().sum().sum()} missing values")

        # Scale returns to avoid numerical precision issues
        pivot_df = pivot_df * 100  # Scale by 100

        # Drop missing values
        pivot_df = pivot_df.dropna(axis=1, how="any")

        if pivot_df.empty:
            print(" Error: No valid data after cleaning!")
            return {"error": "No valid stock return data"}

        print(f" Cleaned Data Shape: {pivot_df.shape}")

        #  Portfolio Optimization using PyPortfolioOpt
        mu = mean_historical_return(pivot_df)
        S = CovarianceShrinkage(pivot_df).ledoit_wolf()

        # Fix: Replace NaN values in covariance matrix
        S = pd.DataFrame(S).fillna(0).values

        # Run optimization
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()

        print(f"✅ Optimized Portfolio Weights: {weights}")

        return {"optimized_weights": weights}

    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        return {"error": str(e)}


    
@app.get("/portfolio-value")
def get_portfolio_value():
    query = """
    SELECT Date, SUM(portfolio_value) AS Portfolio_Value
    FROM deduplicated_holdings
    GROUP BY Date
    ORDER BY Date ASC;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        return {"portfolio_value": [{"date": row[0], "value": row[1]} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/etf-sector-breakdown/{etf}")
def get_etf_sector_breakdown(etf: str):
    """Fetches the sector breakdown for a given ETF."""
    query = f"""
    SELECT Stock, SUM(Weight) AS TotalWeight
    FROM etf_sector_breakdown
    WHERE ETF = '{etf}'
    GROUP BY Stock
    ORDER BY TotalWeight DESC;
    """
    
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()

        if not result:
            raise HTTPException(status_code=404, detail="ETF sector data not found")
        
        return {"etf": etf, "breakdown": [{"stock": row[0], "weight": row[1]} for row in result]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/portfolio-vs-sp500")
def get_portfolio_vs_sp500():
    query = """
    WITH
        spy_prices AS (
            SELECT
                min(Date) AS Trade_Date,
                max(Close) AS Close
            FROM ssmif.stock_prices
            WHERE Symbol = 'SPY'
            GROUP BY Symbol, toYYYYMM(Date)
        ),
        portfolio_values AS (
            SELECT
                Date AS Trade_Date,
                SUM(value) AS Portfolio_Value
            FROM ssmif.expanded_holdings
            GROUP BY Date
        )
    SELECT
        p.Trade_Date,
        (p.Portfolio_Value / first_value(p.Portfolio_Value) OVER (ORDER BY p.Trade_Date ASC)) * 100 AS Portfolio_Performance,
        (s.Close / first_value(s.Close) OVER (ORDER BY s.Trade_Date ASC)) * 100 AS SP500_Performance
    FROM portfolio_values AS p
    INNER JOIN spy_prices AS s ON p.Trade_Date = s.Trade_Date
    ORDER BY p.Trade_Date ASC;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()

        return {
            "performance": [
                {"date": row[0], "portfolio": row[1], "sp500": row[2]} for row in result
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@app.get("/portfolio-value")
def get_portfolio_value():
    query = """
    SELECT Date, SUM(portfolio_value) AS Portfolio_Value
    FROM expanded_holdings
    GROUP BY Date
    ORDER BY Date;
    """
    try:
        client = get_clickhouse_client()  
        result = client.execute(query)
        client.disconnect()  
        return {"portfolio_value": [{"date": row[0], "value": row[1]} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/portfolio-holdings")
def get_portfolio_holdings():
    """
    Fetches the latest portfolio holdings, including shares, latest price, and total value.
    """
    query = """
    WITH latest_prices AS (
        SELECT 
            Symbol,
            Close AS price
        FROM stock_prices
        WHERE Date = (SELECT max(Date) FROM stock_prices)
    )
    SELECT 
        h.Symbol,
        SUM(h.Shares) AS Shares,
        lp.price AS price,
        SUM(h.Shares) * lp.price AS value
    FROM holdings h
    JOIN latest_prices lp ON h.Symbol = lp.Symbol
    GROUP BY h.Symbol, lp.price
    ORDER BY value DESC;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        
        holdings = [
            {"Symbol": row[0], "Shares": row[1], "price": row[2], "value": row[3]} 
            for row in result
        ]
        return {"holdings": holdings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio-trades")
def get_portfolio_trades():
    """
    Fetches all trade transactions.
    """
    query = """
    SELECT 
        Date,
        Symbol,
        CASE 
            WHEN Shares > 0 THEN 'BUY'
            ELSE 'SELL'
        END AS Trade_Type,
        ABS(Shares) AS Shares,
        Close AS Price
    FROM holdings
    JOIN stock_prices USING (Symbol, Date)
    ORDER BY Date DESC
    LIMIT 100;
    """
    
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        
        trades = [
            {"Date": row[0], "Symbol": row[1], "Type": row[2], "Shares": row[3], "Price": row[4]} 
            for row in result
        ]
        return {"trades": trades}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/rolling-volatility")
def get_rolling_volatility():
    query = """
    SELECT Trade_Date, Rolling_Volatility_30D
    FROM (
        SELECT 
            Trade_Date,
            stddevPop(Daily_Return) OVER (ORDER BY Trade_Date ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) AS Rolling_Volatility_30D
        FROM daily_returns
    )
    ORDER BY Trade_Date;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        return {"rolling_volatility": [{"date": row[0], "volatility": row[1]} for row in result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/correlation-sp500")
def get_correlation():
    query = """
    WITH
        daily_spy AS (
            SELECT
                Date AS Trade_Date,
                max(Close) AS Close
            FROM stock_prices
            WHERE Symbol = 'SPY'
            GROUP BY Date
        ),
        sp500_returns AS (
            SELECT
                Trade_Date,
                toDecimal64(
                  (Close - lagInFrame(Close, 1) OVER (ORDER BY Trade_Date ASC)) /
                  lagInFrame(Close, 1) OVER (ORDER BY Trade_Date ASC),
                  18
                ) AS SP500_Return
            FROM daily_spy
        ),
        aggregated_portfolio_returns AS (
            SELECT
                Trade_Date,
                avg(Daily_Return) AS Daily_Return
            FROM daily_returns
            GROUP BY Trade_Date
        ),
        valid_returns AS (
            SELECT
                p.Trade_Date,
                p.Daily_Return,
                toFloat64(s.SP500_Return) AS SP500_Return
            FROM aggregated_portfolio_returns AS p
            INNER JOIN sp500_returns AS s ON p.Trade_Date = s.Trade_Date
            WHERE p.Daily_Return IS NOT NULL
              AND s.SP500_Return IS NOT NULL
              AND p.Trade_Date >= '2020-01-01'
        )
    SELECT
        corr(Daily_Return * 10000, SP500_Return * 10000) AS Correlation_With_SP500,
        stddevPop(Daily_Return * 10000) AS Portfolio_StdDev,
        stddevPop(SP500_Return * 10000) AS SP500_StdDev
    FROM valid_returns;
    """
    try:
        client = get_clickhouse_client()
        result = client.execute(query)
        client.disconnect()
        if result:
            return {
                "correlation_with_sp500": result[0][0],
                "portfolio_stddev": result[0][1],
                "sp500_stddev": result[0][2]
            }
        return {"correlation_with_sp500": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))