import React, { useEffect, useState } from "react";
import StyledBox from "../Stylebox";
import "./Home.css";


export const Home = () => {
  const [movies, setMovies] = useState([]);
  const [actors, setActors] = useState([]);

  useEffect(() => {
    // get top 5
    fetch("http://127.0.0.1:5000/api/movies")
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error("Error fetching movies:", error));

    // get acto
    fetch("http://127.0.0.1:5000/api/actors")
      .then(response => response.json())
      .then(data => setActors(data))
      .catch(error => console.error("Error fetching actors:", error));
  }, []);

  return (
    <div className="home-container">
      
      <h1 className="home-title">TOP FIVE MOVIES</h1>
      <div className="box-container">
        {movies.slice(0, 5).map((movie, index) => (
          <StyledBox 
            key={index} 
            title={movie.name} 
            image={movie.image}  
            description={movie.genre}  
          />
        ))}
      </div>

      
      <h1 className="home-title">TOP FIVE ACTORS</h1>
      <div className="box-container">
        {actors.slice(0, 5).map((actor, index) => (
          <StyledBox 
            key={index} 
            title={actor.name} 
            image={actor.image}  
            description={actor.description}  
          />
        ))}
      </div>
    </div>
  );
};

export default Home;
