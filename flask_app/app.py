from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models.models import db  # Import db from models
from routes.films import films_bp
from routes.actors import actors_bp
from routes.allfilms import allfilms_bp
from routes.customers import customers_bp
from sqlalchemy.sql import text  # ✅ Import text for raw SQL queries

app = Flask(__name__)
CORS(app)

# ✅ MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaobailei1943@127.0.0.1:3306/sakila'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # ✅ Initialize SQLAlchemy with Flask

# ✅ Register Blueprints
app.register_blueprint(films_bp)  
app.register_blueprint(actors_bp)
app.register_blueprint(customers_bp, url_prefix="/api")  
app.register_blueprint(allfilms_bp, url_prefix="/api/allfilms")  

@app.route('/')
def home():
    return "Flask API connected successfully!"

# ✅ Fetch Films Data from MySQL Instead of CSV
@app.route("/api/table", methods=["GET"])
def get_table():
    try:
        query = text("""
            SELECT 
                f.film_id, 
                f.title, 
                f.description, 
                f.release_year, 
                f.rating, 
                f.length, 
                f.rental_duration, 
                f.rental_rate, 
                f.replacement_cost, 
                f.special_features, 
                GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
            FROM film f
            LEFT JOIN film_actor fa ON f.film_id = fa.film_id
            LEFT JOIN actor a ON fa.actor_id = a.actor_id
            GROUP BY f.film_id
        """)

        result = db.session.execute(query).fetchall()

        films = []
        for row in result:
            films.append({
                "film_id": row.film_id,
                "title": row.title,
                "description": row.description,
                "release_year": row.release_year,
                "rating": row.rating,
                "length": row.length,
                "rental_duration": row.rental_duration,
                "rental_rate": row.rental_rate,
                "replacement_cost": row.replacement_cost,
                "special_features": row.special_features,
                "actors": row.actors
            })

        return jsonify(films)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Customers Data from MySQL Instead of CSV
@app.route("/api/customers", methods=["GET"])
def get_customers():
    try:
        query = text("""
            SELECT 
                c.customer_id, 
                c.store_id, 
                c.first_name, 
                c.last_name, 
                c.email, 
                c.address_id, 
                c.active, 
                c.create_date, 
                c.last_update
            FROM customer c
        """)

        result = db.session.execute(query).fetchall()

        customers = []
        for row in result:
            customers.append({
                "customer_id": row.customer_id,
                "store_id": row.store_id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "address_id": row.address_id,
                "active": bool(row.active),
                "create_date": row.create_date.strftime("%Y-%m-%d"),
                "last_update": row.last_update.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(customers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask Application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Ensure tables exist (only needed if using models)
    app.run(debug=True, port=5000)
