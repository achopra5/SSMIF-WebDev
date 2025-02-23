import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from "recharts";
import { fetchDailyReturns } from "../api";

const DailyReturnsChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchDailyReturns().then(setData);
  }, []);

  return (
    <div className="chart-container">
      <h2>Daily Returns Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis tickFormatter={(tick) => `${(tick * 100).toFixed(2)}%`} />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip formatter={(value) => `${(value * 100).toFixed(2)}%`} />
          <Legend />
          <Line type="monotone" dataKey="return" stroke="#82ca9d" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DailyReturnsChart;
