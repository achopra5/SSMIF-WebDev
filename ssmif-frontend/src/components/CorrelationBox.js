import React, { useEffect, useState } from "react";
import { fetchCorrelation } from "../api";

const CorrelationBox = () => {
  const [correlation, setCorrelation] = useState(null);

  useEffect(() => {
    fetchCorrelation().then(setCorrelation);
  }, []);

  return (
    <div>
      <h2>Portfolio Correlation with S&P 500</h2>
      {correlation ? (
        <p>Correlation: {correlation.correlation_with_sp500.toFixed(3)}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default CorrelationBox;
