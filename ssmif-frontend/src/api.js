import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // ✅ Centralized Base URL

export const fetchPortfolioValue = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/portfolio-value`);
    return response.data.portfolio_value || [];
  } catch (error) {
    console.error("Error fetching portfolio value:", error.response?.data || error.message);
    return [];
  }
};

export const fetchDailyReturns = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/daily-returns`);
    return response.data.daily_returns || [];
  } catch (error) {
    console.error("Error fetching daily returns:", error.response?.data || error.message);
    return [];
  }
};

export const fetchCorrelation = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/correlation-sp500`);
    return response.data || null;
  } catch (error) {
    console.error("Error fetching correlation:", error.response?.data || error.message);
    return null;
  }
};

export const fetchRollingVolatility = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/rolling-volatility`);
    return response.data.rolling_volatility || [];
  } catch (error) {
    console.error("Error fetching rolling volatility:", error.response?.data || error.message);
    return [];
  }
};

export const fetchPortfolioVsSP500 = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/portfolio-vs-sp500`);
    return response.data.performance || [];
  } catch (error) {
    console.error("Error fetching portfolio vs S&P 500:", error.response?.data || error.message);
    return [];
  }
};



export const fetchPortfolioHoldings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/portfolio-holdings`);
    return response.data.holdings || [];
  } catch (error) {
    console.error("Error fetching portfolio holdings:", error);
    return [];
  }
};

export const fetchOptimizedPortfolio = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/optimize-portfolio`);
    return response.data.optimized_weights || {};
  } catch (error) {
    console.error("Error fetching optimized portfolio:", error);
    return {};
  }
};


export const fetchSharpeRatio = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/sharpe-ratio");
    if (!response.ok) {
      throw new Error("API Request Failed");
    }
    return await response.json();
  } catch (error) {
    console.error(" API Fetch Error:", error);
    return { sharpe_ratio: [] }; // Return empty array if error occurs
  }
};


// ✅ Fetch Trade Transactions
export const fetchPortfolioTrades = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/portfolio-trades`);
    return response.data.trades || [];
  } catch (error) {
    console.error("Error fetching portfolio trades:", error);
    return [];
  }
};
