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
import { fetchRollingVolatility } from "../api";

const RollingVolatilityChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRollingVolatility()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="chart-container">
      <h2> Rolling 30-Day Volatility</h2>

      {loading && <p>Loading volatility data...</p>}
      {!loading && data.length === 0 && <p>No volatility data available.</p>}

      {data.length > 0 && (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip formatter={(value) => `${(value * 100).toFixed(2)}%`} />
            <Legend />
            <Line type="monotone" dataKey="volatility" stroke="#FF7300" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default RollingVolatilityChart;
