import React, { useEffect, useState } from "react";
import "./FilmTable.css";  // ✅ Ensure CSS file exists

const FilmTable = () => {
  const [films, setFilms] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const filmsPerPage = 5;  // ✅ Same as customers table

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/table")
      .then(response => response.json())
      .then(data => {
        console.log("Fetched films:", data);
        setFilms(Array.isArray(data) ? data : []);
      })
      .catch(error => {
        console.error("Error fetching films:", error);
        setFilms([]);
      });
  }, []);

  if (!Array.isArray(films)) {
    console.error("films is not an array:", films);
    return <p>Loading failed. Please check API.</p>;
  }

  // 🔥 Filter films based on search query (title, actors, or rating)
  const filteredFilms = films.filter(film =>
    film.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    film.actors?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    film.rating?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // 📌 Pagination logic
  const totalPages = Math.ceil(filteredFilms.length / filmsPerPage);
  const startIndex = (currentPage - 1) * filmsPerPage;
  const endIndex = startIndex + filmsPerPage;
  const currentFilms = filteredFilms.slice(startIndex, endIndex);

  const goToPreviousPage = () => setCurrentPage(prev => Math.max(prev - 1, 1));
  const goToNextPage = () => setCurrentPage(prev => Math.min(prev + 1, totalPages));

  return (
    <div className="film-table-container">
      <h2>Film Information</h2>
      <input
        type="text"
        placeholder="Search film by title, actor, or rating..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="search-box"
      />
      <table className="film-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Release Year</th>
            <th>Rating</th>
            <th>Length</th>
            <th>Rental Duration</th>
            <th>Rental Rate</th>
            <th>Replacement Cost</th>
            <th>Special Features</th>
            <th>Actors</th>
          </tr>
        </thead>
        <tbody>
          {currentFilms.length > 0 ? (
            currentFilms.map((film, index) => (
              <tr key={index}>
                <td>{film.film_id}</td>
                <td>{film.title}</td>
                <td>{film.description}</td>
                <td>{film.release_year}</td>
                <td>{film.rating}</td>
                <td>{film.length}</td>
                <td>{film.rental_duration}</td>
                <td>{film.rental_rate}</td>
                <td>{film.replacement_cost}</td>
                <td>{film.special_features}</td>
                <td>{film.actors || "No actors listed"}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="11" className="no-results">No films found</td>
            </tr>
          )}
        </tbody>
      </table>

      {/* 📌 Pagination Controls */}
      <div className="pagination">
        <button onClick={goToPreviousPage} disabled={currentPage === 1}>Previous</button>
        <span>Page {currentPage} of {totalPages}</span>
        <button onClick={goToNextPage} disabled={currentPage === totalPages}>Next</button>
      </div>
    </div>
  );
};

export default FilmTable;
