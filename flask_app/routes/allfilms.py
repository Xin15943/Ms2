from flask import Blueprint, jsonify, request
from models.models import db
from sqlalchemy.sql import text

# ✅ Ensure Blueprint name is correct
allfilms_bp = Blueprint('allfilms_bp', __name__)  

# ✅ Get All Films with Details
@allfilms_bp.route('/details', methods=['GET'])
def get_all_films():
    query = text("""
        SELECT 
            f.film_id AS movie_id, 
            f.title, 
            f.description, 
            f.release_year, 
            f.rating AS rate, 
            f.length AS time, 
            f.rental_rate AS price,
            COALESCE(GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', '), 'No Actors') AS main_actors
        FROM film f
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
        GROUP BY f.film_id
    """)

    result = db.session.execute(query).fetchall()

    if not result:
        return jsonify({"error": "No movies found"}), 404  # ✅ Handle empty database

    films = []
    for row in result:
        films.append({
            "movie_id": row.movie_id,
            "title": row.title,
            "description": row.description,
            "release_year": row.release_year,
            "rate": row.rate,
            "time": row.time,
            "price": row.price,
            "main_actors": row.main_actors
        })

    return jsonify(films)


# ✅ Search Films by Title or Actor
@allfilms_bp.route('/search', methods=['GET'])
def search_films():
    search_query = request.args.get('query', '').strip()

    if not search_query:
        return jsonify({"error": "No search query provided"}), 400  # ✅ Prevent empty searches

    query = text("""
        SELECT 
            f.film_id AS movie_id, 
            f.title, 
            f.description, 
            f.release_year, 
            f.rating AS rate, 
            f.length AS time, 
            f.rental_rate AS price,
            COALESCE(GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', '), 'No Actors') AS main_actors
        FROM film f
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
        WHERE LOWER(f.title) LIKE LOWER(:search_query) 
           OR LOWER(a.first_name) LIKE LOWER(:search_query) 
           OR LOWER(a.last_name) LIKE LOWER(:search_query)
        GROUP BY f.film_id
    """)

    result = db.session.execute(query, {"search_query": f"%{search_query}%"}).fetchall()

    films = []
    for row in result:
        films.append({
            "movie_id": row.movie_id,
            "title": row.title,
            "description": row.description,
            "release_year": row.release_year,
            "rate": row.rate,
            "time": row.time,
            "price": row.price,
            "main_actors": row.main_actors
        })

    return jsonify(films)
