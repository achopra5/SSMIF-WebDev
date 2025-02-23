import React, { useState, useEffect } from "react";
import PortfolioChart from "../components/PortfolioChart";
import DailyReturnsChart from "../components/DailyReturnsChart";
import CorrelationBox from "../components/CorrelationBox";
import RollingVolatilityChart from "../components/RollingVolatilityChart";
import PortfolioVsSP500 from "../components/PortfolioVsSP500";
import HoldingsTable from "../components/HoldingsTable";
import TradesTable from "../components/TradesTable";
import SharpeRatioChart from "../components/SharpeRatioChart"; 
import OptimizedPortfolio from "../components/OptimizedPortfolio";
import "./dashboard.css";

const Dashboard = () => {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("darkMode") === "true";
  });

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  return (
    <div className="dashboard-container">
      <button onClick={() => setDarkMode(!darkMode)} className="toggle-btn">
        {darkMode ? "🌞 Light Mode" : "🌙 Dark Mode"}
      </button>

      <h1>SSMIF Portfolio Dashboard</h1>

      {/* KPI Metrics */}
      <div className="kpi-container">
        <div className="kpi-card">
          <h3>Total Portfolio Value</h3>
          <p>$101,629,475</p>
        </div>
        <div className="kpi-card">
          <h3>Portfolio Return</h3>
          <p>+12.5%</p>
        </div>
        <div className="kpi-card">
          <h3>Volatility</h3>
          <p>8.2%</p>
        </div>
        <div className="kpi-card">
          <h3>Sharpe Ratio</h3>
          <p>1.52</p>
        </div>
      </div>

      {/* Holdings and Trades Tables */}
      <div className="section">
        <div className="table-container"><HoldingsTable /></div>
        <div className="table-container"><TradesTable /></div>
      </div>

      {/* Charts Row 1 */}
      <div className="chart-row">
        <div className="chart-card"><PortfolioChart /></div>
        <div className="chart-card"><DailyReturnsChart /></div>
      </div>

      {/* Sharpe Ratio Chart */}
      <div className="chart-row">
        <div className="chart-card"><SharpeRatioChart /></div>
      </div>

      {/* Charts Row 2 */}
      <div className="chart-row">
        <div className="chart-card"><RollingVolatilityChart /></div>
      </div>

      {/* Portfolio vs S&P 500 */}
      <div className="chart-large">
        <div><CorrelationBox /></div>
        <div className="chart-card"><PortfolioVsSP500 /></div>
      </div>
    </div>
  );
};

export default Dashboard;