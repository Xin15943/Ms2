from flask import Blueprint, jsonify
from models.models import db
from sqlalchemy.sql import text

actors_bp = Blueprint('actors', __name__)

@actors_bp.route('/api/actors/top', methods=['GET'])
def get_top_actors_with_movies():
    query = text("""
        WITH top_actors AS (
            SELECT a.actor_id, a.first_name, a.last_name, COUNT(r.rental_id) AS rental_count
            FROM actor a
            JOIN film_actor fa ON a.actor_id = fa.actor_id
            JOIN inventory i ON fa.film_id = i.film_id
            JOIN rental r ON i.inventory_id = r.inventory_id
            GROUP BY a.actor_id
            ORDER BY rental_count DESC
            LIMIT 5
        )
        SELECT ta.actor_id, ta.first_name, ta.last_name, f.title AS film_title, COUNT(r.rental_id) AS movie_rentals
        FROM top_actors ta
        JOIN film_actor fa ON ta.actor_id = fa.actor_id
        JOIN film f ON fa.film_id = f.film_id
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        GROUP BY ta.actor_id, f.film_id
        ORDER BY ta.actor_id, movie_rentals DESC;
    """)

    result = db.session.execute(query).fetchall()

    # Organize data into correct JSON format
    actor_dict = {}
    for row in result:
        actor_id = row.actor_id
        if actor_id not in actor_dict:
            actor_dict[actor_id] = {
                "id": actor_id,
                "name": f"{row.first_name} {row.last_name}",
                "top_movies": []
            }
        if len(actor_dict[actor_id]["top_movies"]) < 5:
            actor_dict[actor_id]["top_movies"].append(row.film_title)

    return jsonify(list(actor_dict.values()))
