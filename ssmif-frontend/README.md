# **SSMIF Quant Development Challenge - README**

## **📌 Project Overview**
This project is submitted as part of the **SSMIF Quant Development Challenge - Spring 2025**. The objective is to build a **full-stack financial application** that tracks a model portfolio’s performance, sector breakdown, and historical returns using **FastAPI, ClickHouse, React, and PyPortfolioOpt**.

---

## **🛠️ Technologies Used**
### **Backend**
- **FastAPI** - API framework for Python
- **ClickHouse** - Time-series database for storing financial data
- **yFinance** - Fetching stock price data
- **PyPortfolioOpt** - Portfolio optimization

### **Frontend**
- **React.js** - Frontend framework
- **Recharts** - Data visualization for financial charts
- **Axios** - API requests handling

### **DevOps & Deployment**
- **Docker** - Containerization (if applicable)
- **Git** - Version control

---

## **📂 Project Structure**
```
ssmif-quant-dev/
│── backend/
│   ├── main.py          # FastAPI backend
│   ├── database.py      # ClickHouse setup
│   ├── services/
│   │   ├── fetch_stock_prices.py # Fetch stock prices
│   │   ├── load_holdings.py  # Load holdings into ClickHouse
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PortfolioChart.js
│   │   │   ├── DailyReturnsChart.js
│   │   │   ├── HoldingsTable.js
│   │   │   ├── TradesTable.js
│   │   │   ├── CorrelationBox.js
│   │   │   ├── PortfolioVsSP500.js
│   │   │   ├── SharpeRatioChart.js
│   │   │   ├── OptimizedPortfolio.js
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   ├── App.js  # Main app entry
│   │   ├── api.js  # API calls for frontend
│   │   ├── index.js  # React root file
│   │   ├── styles/
│   │   │   ├── dashboard.css  # Dashboard styling
│   │   │   ├── index.css  # Global styles
│   │   │   ├── TradesTable.css  # Trades table styling
│── requirements.txt
│── README.md
│── CITATIONS.md
```

---

## **📊 Features Implemented**
- **Historical Portfolio Value** - Tracks performance over time
- **Sector Breakdown Over Time** - Portfolio sector exposure
- **Portfolio Performance vs. S&P 500** - Benchmark comparison
- **Optimized Portfolio Weights** - Using PyPortfolioOpt
- **Risk Metrics Computation** - Volatility, Sharpe Ratio, and Max Drawdown
- **Trade Tracking** - Log past and current trades

---

## **⚙️ Installation & Setup**
### **Backend Setup**
```sh
pip install -r requirements.txt
uvicorn main:app --reload
```

### **Frontend Setup**
```sh
npm install
npm start
```

### **Database Setup (ClickHouse)**
```sh
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
docker exec -it clickhouse-server clickhouse-client
```

---

## **🚀 API Endpoints**
### **Portfolio API**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/portfolio-value` | GET | Returns portfolio value over time |
| `/daily-returns` | GET | Returns daily returns |
| `/correlation-sp500` | GET | Returns portfolio correlation with S&P 500 |
| `/optimize-portfolio` | GET | Returns optimized portfolio weights |

---

CHATGPT citations

print(f"✅ Optimized Portfolio Weights: {weights}")

        return {"optimized_weights": weights}

    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        return {"error": str(e)}


---

## **📩 Questions & Contact**
If you have any questions, please reach out via email.  
🔗 **Submission Link:** [Google Form](https://forms.gle/RHJzrUPQutphFUZS9)  
📧 **Contact:** sparikh10@stevens.edu (Head of Quant)

---

🚀 **Good luck with your submission!** 🎯
