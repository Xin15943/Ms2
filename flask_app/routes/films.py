from flask import Blueprint, jsonify, request
from models.models import db
from sqlalchemy.sql import text

films_bp = Blueprint('films', __name__)

# ✅ Existing API - Get Top 5 Rented Movies
@films_bp.route('/api/films/top_rented', methods=['GET'])
def get_top_rented_films():
    query = text("""
        SELECT f.film_id AS id, f.title, f.release_year, f.rental_rate, f.length, 
               COUNT(r.rental_id) AS rental_count
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        GROUP BY f.film_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """)

    result = db.session.execute(query).fetchall()

    film_list = [
        {
            "id": film.id,
            "title": film.title,
            "release_year": film.release_year,
            "rental_rate": film.rental_rate,
            "length": film.length,
            "rental_count": film.rental_count,
            "image": f"movies/{film.title.lower().replace(' ', '-')}.jpg"
        }
        for film in result
    ]

    return jsonify(film_list)


# ✅ NEW API - Get ALL Films with Details
@films_bp.route('/api/films', methods=['GET'])
def get_all_films():
    query = text("""
        SELECT 
            f.film_id AS movie_id, 
            f.title, 
            f.description, 
            f.release_year, 
            f.rating AS rate, 
            f.length AS time, 
            f.rental_rate AS price
        FROM film f
    """)

    result = db.session.execute(query).fetchall()

    films = []
    for row in result:
        films.append({
            "movie_id": row.movie_id,
            "title": row.title,
            "description": row.description,
            "release_year": row.release_year,
            "rate": row.rate,
            "time": row.time,
            "price": row.price
        })

    return jsonify(films)


# ✅ NEW API - Get Film Details by Film ID
@films_bp.route('/api/films/<int:film_id>', methods=['GET'])
def get_film_details(film_id):
    query = text("""
        SELECT 
            f.film_id AS movie_id, 
            f.title, 
            f.description, 
            f.release_year, 
            f.rating AS rate, 
            f.length AS time, 
            f.rental_rate AS price
        FROM film f
        WHERE f.film_id = :film_id
    """)

    result = db.session.execute(query, {"film_id": film_id}).fetchone()

    if not result:
        return jsonify({"error": "Film not found"}), 404

    # ✅ Get Main Actors for the Film
    actors_query = text("""
        SELECT a.first_name, a.last_name
        FROM actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        WHERE fa.film_id = :film_id
    """)

    actors_result = db.session.execute(actors_query, {"film_id": film_id}).fetchall()

    actors = [f"{actor.first_name} {actor.last_name}" for actor in actors_result]

    film_details = {
        "movie_id": result.movie_id,
        "title": result.title,
        "description": result.description,
        "release_year": result.release_year,
        "rate": result.rate,
        "time": result.time,
        "price": result.price,
        "main_actors": actors
    }

    return jsonify(film_details)
