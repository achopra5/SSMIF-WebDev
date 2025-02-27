# SSMIF-WebDev - Quant Development Challenge Submission

## Overview
This project is part of the **SSMIF Quant Development Challenge (Spring 2025)**.  
It is a **full-stack financial application** designed to:
- Fetch historical stock data from **Yahoo Finance** 
- Store & process financial data using **ClickHouse**
- Provide **real-time portfolio performance insights** via a **React frontend**
- Support **portfolio optimization & risk analysis** 

---

## 📂 Project Structure
SSMIF-DEV/
│── ssmif-backend/               # FastAPI backend
│   ├── __pycache__/             # Compiled Python files
│   ├── fetch_stock_prices.py    # Stock data ingestion
│   ├── load_holdings.py         # Holdings ingestion
│   ├── main.py                  # API entry point
│── ssmif-frontend/              # React frontend
│   ├── node_modules/            # Dependencies
│   ├── public/                  # Static assets
│   │   ├── favicon.ico          
│   │   ├── index.html           # Main HTML file
│   │   ├── manifest.json        
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── CorrelationBox.js
│   │   │   ├── DailyReturnsChart.js
│   │   │   ├── HoldingsTable.js
│   │   │   ├── OptimizedPortfolio.js
│   │   │   ├── PortfolioChart.js
│   │   │   ├── PortfolioVsSP500.js
│   │   │   ├── RollingVolatilityChart.js
│   │   │   ├── SharpeRatioChart.js
│   │   │   ├── TradesTable.js
│   │   │   ├── TradesTable.css   # Table styles
│   │   ├── pages/               # Main pages
│   │   │   ├── Dashboard.js
│   │   ├── api.js               # API calls
│   │   ├── App.js               # Main App component
│   │   ├── index.js             # React root file
│   │   ├── styles/
│   │   │   ├── dashboard.css    # Dashboard styles
│   │   │   ├── index.css        # Global styles
│   ├── package.json             # Frontend dependencies
|---

Setup Instructions
Backend (FastAPI + ClickHouse)
Install dependencies
fastapi
clickhouse-driver
pandas
yfinance
uvicorn
pypfopt
requests
python-dotenv



Start FastAPI server
uvicorn main:app --reload

Frontend (React)
Install dependencies
cd ssmif-frontend
npm install

Run the frontend

npm start

Features
Fetches historical stock prices
Stores financial data in ClickHouse
Calculates portfolio value & returns
Plots Sharpe ratio & risk metrics
Displays optimized portfolio allocations


![image](https://github.com/user-attachments/assets/830a41d6-c4b4-45b7-ac95-931fd74a24a9)
![image](https://github.com/user-attachments/assets/0c834b0f-5524-4acb-af98-6451a13c0322)
![image](https://github.com/user-attachments/assets/108e81c1-2811-46fd-b71b-55bfa6fa8c33)
![image](https://github.com/user-attachments/assets/e9b84384-e65a-4ef5-9dbd-ccf22f9b62e6)
![image](https://github.com/user-attachments/assets/10b3527c-7a94-47db-bad6-36d59a257c91)
![image](https://github.com/user-attachments/assets/2ddbd2b2-7784-4329-b2d8-3885d2cc794e)







