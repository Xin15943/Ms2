import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import StyledBox from "../Stylebox";
import "./Home.css";

export const Home = () => {
  const [movies, setMovies] = useState([]);
  const [actors, setActors] = useState([]);

  // Fetch Top 5 Movies
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/films/top_rented")
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error("Error fetching movies:", error));
  }, []);

  // Fetch Top 5 Actors
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/actors/top")  // ✅ Use `/api/actors/top`
      .then(response => response.json())
      .then(data => setActors(data))
      .catch(error => console.error("Error fetching actors:", error));
  }, []);

  return (
    <div className="home-container">
      <h1 className="home-title">TOP FIVE MOVIES</h1>
      <div className="box-container">
        {movies.length > 0 ? (
          movies.map((movie, index) => (
            <StyledBox 
              key={index} 
              title={movie.title}  
              image="/11.jpg"  
              description={`📅 Year: ${movie.release_year} 
                🎟️ Rental Rate: $${movie.rental_rate} 
                ⏳ Length: ${movie.length} min
                🔥 Rented ${movie.rental_count} times`}  
            />
          ))
        ) : (
          <p>Loading movies...</p>
        )}
      </div>

      <h1 className="home-title">TOP FIVE ACTORS</h1>
      <div className="box-container">
        {actors.length > 0 ? (
          actors.map((actor, index) => (
            <StyledBox 
              key={index} 
              title={actor.name}  
              image="1.jpg"  
              description={`🎬 Top 5 Movies:
                1️⃣ ${actor.top_movies?.[0] || "N/A"}
                2️⃣ ${actor.top_movies?.[1] || "N/A"}
                3️⃣ ${actor.top_movies?.[2] || "N/A"}
                4️⃣ ${actor.top_movies?.[3] || "N/A"}
                5️⃣ ${actor.top_movies?.[4] || "N/A"}`}  
            />
          ))
        ) : (
          <p>Loading actors...</p>
        )}
      </div>
    </div>
  );
};

export default Home;
