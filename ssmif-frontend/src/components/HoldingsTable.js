import React, { useEffect, useState } from "react";
import { fetchPortfolioHoldings } from "../api";


const HoldingsTable = () => {
  const [holdings, setHoldings] = useState([]);
  const [filteredHoldings, setFilteredHoldings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortKey, setSortKey] = useState("value");
  const [sortOrder, setSortOrder] = useState("desc");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchPortfolioHoldings().then((data) => {
      setHoldings(data);
      setFilteredHoldings(data);
      setLoading(false);
    });
  }, []);

  const handleSort = (key) => {
    const order = sortKey === key && sortOrder === "asc" ? "desc" : "asc";
    setSortKey(key);
    setSortOrder(order);

    const sortedHoldings = [...filteredHoldings].sort((a, b) => {
      if (order === "asc") return a[key] > b[key] ? 1 : -1;
      return a[key] < b[key] ? 1 : -1;
    });

    setFilteredHoldings(sortedHoldings);
  };

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = holdings.filter((h) =>
      h.Symbol.toLowerCase().includes(term)
    );
    setFilteredHoldings(filtered);
  };

  return (
    <div className="holdings-container">
      <h2>📜 Portfolio Holdings</h2>
      
      {/* Search Input */}
      <input
        type="text"
        placeholder="Search by Symbol..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
      />

      {loading ? (
        <p>Loading holdings...</p>
      ) : (
        <table className="holdings-table">
          <thead>
            <tr>
              <th onClick={() => handleSort("Symbol")}>Symbol ⬍</th>
              <th onClick={() => handleSort("Shares")}>Shares ⬍</th>
              <th onClick={() => handleSort("price")}>Market Price ⬍</th>
              <th onClick={() => handleSort("value")}>Total Value ⬍</th>
            </tr>
          </thead>
          <tbody>
            {filteredHoldings.map((h, index) => (
              <tr key={index}>
                <td>{h.Symbol}</td>
                <td>{h.Shares.toLocaleString()}</td>
                <td>${h.price?.toFixed(2)}</td>
                <td>${h.value?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default HoldingsTable;
