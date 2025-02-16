import React, { useEffect, useState } from "react";
import "./TableComponent.css";  

const TableComponent = () => {
  const [data, setData] = useState([]);  
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/table")  
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data);
        if (Array.isArray(data)) {
          setData(data);
        } else {
          console.error("API wrong type data:", data);
          setData([]);  
        }
      })
      .catch(error => {
        console.error("Error fetching data:", error);
        setData([]);  
      });
  }, []);

  if (!Array.isArray(data)) {
    console.error("data :", data);
    return <p>fail to </p>;
  }

  // search filter the name and actor
  const filteredData = data.filter(movie =>
    movie.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||   // how to search movie name 
    movie.actors?.some(actor => actor.toLowerCase().includes(searchQuery.toLowerCase()))  // search actors name
  );

  return (
    <div className="table-container">
      <h2>Movie</h2>
      <input
        type="text"
        placeholder="Moive name or Actor name..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="search-box"
      />
      <table className="movie-table">
        <thead>
          <tr>
            <th>Moive ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Year Realase</th>
            <th>Rate</th>
            <th>Time</th>
            <th>Price</th>
            <th>Main Actors</th>  
          </tr>
        </thead>
        <tbody>
          {filteredData.length > 0 ? (
            filteredData.map((movie, index) => (
              <tr key={index}>
                <td>{movie.film_id}</td>
                <td>{movie.title}</td>
                <td>{movie.description}</td>
                <td>{movie.release_year}</td>
                <td>{movie.rating}</td>
                <td>{movie.length}</td>
                <td>{movie.rental_rate}</td>
                <td>{movie.actors ? movie.actors.join(", ") : "None"}</td>  
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="8" className="no-results">can't find it </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
