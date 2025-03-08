import React from "react";
import FilmTable from "../FilmTable";  // ✅ Ensure correct import
import "./Film.css";  // ✅ Ensure Film.css exists

const Film = () => {
  return (
    <div className="film-container">
      <h1>Films</h1>
      <FilmTable />
    </div>
  );
};

export default Film;
