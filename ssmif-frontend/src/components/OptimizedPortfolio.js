import React, { useEffect, useState } from "react";
import { fetchOptimizedPortfolio } from "../api";

const OptimizedPortfolio = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    fetchOptimizedPortfolio().then(setData);
  }, []);

  return (
    <div className="trade-signals">
      <h2>Optimized Portfolio Weights</h2>
      <ul>
        {Object.entries(data).map(([symbol, weight]) => (
          <li key={symbol}>
            {symbol}: {(weight * 100).toFixed(2)}%
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OptimizedPortfolio;
