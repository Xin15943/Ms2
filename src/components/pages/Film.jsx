import React from "react";
import TableComponent from "../TableComponent";  
import "./Film.css";  

const Film = () => {
  return (
    <div className="film-container">
      <h1>MOVIES</h1>
      <TableComponent />  
    </div>
  );
};

export default Film;
