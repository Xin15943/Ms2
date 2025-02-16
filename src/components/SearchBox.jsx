import React from "react";
import "./SearchBox.css";  

const SearchBox = ({ searchTerm, setSearchTerm }) => {
  return (
    <input
      type="text"
      placeholder="Search for a movie..."
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      className="search-box"
    />
  );
};

export default SearchBox;
