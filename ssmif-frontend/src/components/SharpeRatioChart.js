import React, { useEffect, useState } from "react";
import { fetchSharpeRatio } from "../api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";

const SharpeRatioChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetchSharpeRatio();
        console.log(" API Response:", response);
        let rawData = response.sharpe_ratio;

        // Compute a 90-day moving average for smoother trends
        rawData = rawData.map((row, index, arr) => {
          const start = Math.max(0, index - 89); // 90-day rolling window
          const windowData = arr.slice(start, index + 1).map((d) => d.sharpe_ratio);
          return {
            ...row,
            moving_avg: windowData.reduce((sum, val) => sum + val, 0) / windowData.length,
          };
        });

        setData(rawData);
      } catch (error) {
        console.error(" Error fetching Sharpe Ratio:", error);
      }
    };
    loadData();
  }, []);

  return (
    <div className="chart-container">
      <h2> Rolling Sharpe Ratio</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <XAxis
            dataKey="date"
            tickFormatter={(tick) => tick.substring(0, 4)} // Show only the year
            //angle={-45}
            textAnchor="end"
          />
          <YAxis domain={[-6, 18]} tickCount={6} />
          <Tooltip formatter={(value) => value.toFixed(2)} />
          <CartesianGrid strokeDasharray="3 3" />
          <Legend verticalAlign="top" />
          
          {/* Original Sharpe Ratio (light purple) */}
          <Line type="monotone" dataKey="sharpe_ratio" stroke="#8884d8" strokeWidth={1} dot={false} />

          {/* Moving Average for Trend (bold blue) */}
          <Line type="monotone" dataKey="moving_avg" stroke="#0077b6" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SharpeRatioChart;
