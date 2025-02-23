import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { fetchPortfolioVsSP500 } from "../api";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const PortfolioVsSP500 = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchPortfolioVsSP500().then(setData);
  }, []);

  if (!data || data.length < 2) {
    return <p>Not enough data to display</p>;
  }

  const computedData = data.slice(1).map((item, index) => ({
    date: item.date,
    portfolio_return: ((item.portfolio - data[index].portfolio) / data[index].portfolio) * 100,
    sp500_return: ((item.sp500 - data[index].sp500) / data[index].sp500) * 100,
  }));

  const chartData = {
    labels: computedData.map((item) => item.date),
    datasets: [
      {
        label: "Portfolio Returns",
        data: computedData.map((item) => item.portfolio_return),
        borderColor: "#4CAF50",
        borderWidth: 2,
        fill: false,
      },
      {
        label: "S&P 500 Returns",
        data: computedData.map((item) => item.sp500_return),
        borderColor: "#F44336",
        borderWidth: 2,
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: { legend: { display: true } },
    scales: {
      x: { title: { display: true, text: "Date" } },
      y: { title: { display: true, text: "Returns (%)" } },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default PortfolioVsSP500;
