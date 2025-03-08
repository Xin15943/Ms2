import React from "react";

const TableComponent = ({ films }) => {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Year</th>
            <th>Rating</th>
            <th>Duration (min)</th>
            <th>Price ($)</th>
            <th>Main Actors</th>
          </tr>
        </thead>
        <tbody>
          {films.length > 0 ? (
            films.map((film) => (
              <tr key={film.movie_id}>
                <td>{film.movie_id}</td>
                <td>{film.title}</td>
                <td>{film.description}</td>
                <td>{film.release_year}</td>
                <td>{film.rate}</td>
                <td>{film.time}</td>
                <td>{film.price}</td>
                <td>{film.main_actors}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="8">No movies found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
