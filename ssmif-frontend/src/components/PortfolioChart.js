import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
  AreaChart,
  Area
} from "recharts";
import { fetchPortfolioValue } from "../api";

const PortfolioChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchPortfolioValue().then(setData);
  }, []);

  return (
    <div className="chart-container">
      <h2>📈 Portfolio Value Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <XAxis dataKey="date" />
          <YAxis domain={["auto", "auto"]} />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
          <Legend />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            fillOpacity={1}
            fill="url(#colorValue)"
            strokeWidth={2}
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PortfolioChart;
