import React, { useEffect, useState } from "react";
import { fetchPortfolioTrades } from "../api";
import "./TradesTable.css"; // Ensure you create this CSS file for styling

const TradesTable = () => {
  const [trades, setTrades] = useState([]);
  const [filteredTrades, setFilteredTrades] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortKey, setSortKey] = useState("Date");
  const [sortOrder, setSortOrder] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const tradesPerPage = 20;

  useEffect(() => {
    fetchPortfolioTrades().then((data) => {
      setTrades(data);
      setFilteredTrades(data);
    });
  }, []);

  // Sorting logic
  const handleSort = (key) => {
    const order = sortKey === key && sortOrder === "asc" ? "desc" : "asc";
    setSortKey(key);
    setSortOrder(order);

    const sortedTrades = [...filteredTrades].sort((a, b) => {
      if (order === "asc") return a[key] > b[key] ? 1 : -1;
      return a[key] < b[key] ? -1 : 1;
    });

    setFilteredTrades(sortedTrades);
  };

  // Search filter
  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);

    const filtered = trades.filter(
      (trade) =>
        trade.Symbol.toLowerCase().includes(term) ||
        trade.Type.toLowerCase().includes(term) ||
        trade.Date.includes(term)
    );

    setFilteredTrades(filtered);
  };

  // Pagination logic
  const indexOfLastTrade = currentPage * tradesPerPage;
  const indexOfFirstTrade = indexOfLastTrade - tradesPerPage;
  const currentTrades = filteredTrades.slice(indexOfFirstTrade, indexOfLastTrade);

  const totalPages = Math.ceil(filteredTrades.length / tradesPerPage);

  return (
    <div className="trades-container">
      <h2>💰 Trade History</h2>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search by Symbol, Type, Date..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
      />

      {/* Trade Table */}
      <table className="trades-table">
        <thead>
          <tr>
            <th onClick={() => handleSort("Date")}>Date ⬍</th>
            <th onClick={() => handleSort("Symbol")}>Symbol ⬍</th>
            <th onClick={() => handleSort("Type")}>Type ⬍</th>
            <th onClick={() => handleSort("Shares")}>Shares ⬍</th>
            <th onClick={() => handleSort("Price")}>Price ⬍</th>
          </tr>
        </thead>
        <tbody>
          {currentTrades.map((t, index) => (
            <tr key={index}>
              <td>{t.Date}</td>
              <td>{t.Symbol}</td>
              <td className={t.Type === "BUY" ? "buy" : "sell"}>{t.Type}</td>
              <td>{t.Shares.toLocaleString()}</td>
              <td>${t.Price?.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination Controls */}
      <div className="pagination">
        <button onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1}>
          ◀ Prev
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} disabled={currentPage === totalPages}>
          Next ▶
        </button>
      </div>
    </div>
  );
};

export default TradesTable;
