from flask import Blueprint, request, jsonify
from models.models import db
from sqlalchemy.sql import text
from flask_cors import cross_origin

customers_bp = Blueprint('customers_bp', __name__)

# ✅ Get Customers with Pagination & Search
@customers_bp.route('/customers', methods=['GET'])
def get_all_customers():
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 5, type=int)
        search = request.args.get('search', '', type=str)
        offset = (page - 1) * size

        # Query to count total customers matching the search criteria
        count_query = text("""
            SELECT COUNT(*) FROM customer c
            WHERE 
                c.first_name LIKE :search OR 
                c.last_name LIKE :search OR 
                CAST(c.customer_id AS CHAR) LIKE :search
        """)

        search_param = f"%{search}%" if search else "%"

        total_customers = db.session.execute(count_query, {"search": search_param}).scalar()
        total_pages = (total_customers + size - 1) // size  # 🔥 Calculate total pages correctly

        # Query to get paginated customers
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
                c.last_update,
                CASE 
                    WHEN EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = c.customer_id) THEN 1 
                    ELSE 0 
                END AS has_rented_movies,
                CASE 
                    WHEN EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = c.customer_id AND r.return_date IS NULL) THEN 0
                    ELSE 1 
                END AS has_returned_movies
            FROM customer c
            WHERE 
                c.first_name LIKE :search OR 
                c.last_name LIKE :search OR 
                CAST(c.customer_id AS CHAR) LIKE :search
            ORDER BY c.customer_id
            LIMIT :size OFFSET :offset
        """)

        result = db.session.execute(query, {"search": search_param, "size": size, "offset": offset}).fetchall()

        customers = [
            {
                "customer_id": row.customer_id,
                "store_id": row.store_id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "address_id": row.address_id,
                "active": bool(row.active),
                "create_date": row.create_date.strftime("%Y-%m-%d"),
                "last_update": row.last_update.strftime("%Y-%m-%d %H:%M:%S"),
                "has_rented_movies": bool(row.has_rented_movies),
                "has_returned_movies": bool(row.has_returned_movies)
            }
            for row in result
        ]

        return jsonify({"customers": customers, "total_pages": total_pages})

    except Exception as e:
        return jsonify({"error": str(e)}), 500





# ✅ Add New Customer (POST)
@customers_bp.route('/customers', methods=['POST'])
@cross_origin()
def add_customer():
    try:
        data = request.get_json()

        required_fields = ["store_id", "first_name", "last_name", "email", "address_id"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        query = text("""
            INSERT INTO customer (store_id, first_name, last_name, email, address_id, active, create_date, last_update)
            VALUES (:store_id, :first_name, :last_name, :email, :address_id, :active, NOW(), NOW())
        """)

        db.session.execute(query, {
            "store_id": data["store_id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "address_id": data["address_id"],
            "active": data.get("active", 1)  # Default active=1 if not provided
        })

        db.session.commit()
        return jsonify({"message": "Customer added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ✅ Edit Customer (PUT)
@customers_bp.route('/customers/<int:customer_id>', methods=['PUT', 'OPTIONS'])
@cross_origin()
def update_customer(customer_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    try:
        data = request.get_json()

        # Check if customer exists
        check_query = text("SELECT * FROM customer WHERE customer_id = :customer_id")
        result = db.session.execute(check_query, {"customer_id": customer_id}).fetchone()

        if not result:
            return jsonify({"error": "Customer not found"}), 404

        # Update query
        update_query = text("""
            UPDATE customer 
            SET first_name = :first_name, 
                last_name = :last_name, 
                email = :email, 
                store_id = :store_id, 
                address_id = :address_id, 
                active = :active,
                last_update = NOW()
            WHERE customer_id = :customer_id
        """)

        db.session.execute(update_query, {
            "customer_id": customer_id,
            "first_name": data.get("first_name", result.first_name),
            "last_name": data.get("last_name", result.last_name),
            "email": data.get("email", result.email),
            "store_id": data.get("store_id", result.store_id),
            "address_id": data.get("address_id", result.address_id),
            "active": data.get("active", result.active),
        })

        db.session.commit()
        return jsonify({"message": f"Customer ID {customer_id} updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ✅ Delete Customer (DELETE)
@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def delete_customer(customer_id):
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    try:
        print(f"🔍 Checking if customer {customer_id} exists...")

        # Step 1️⃣: Check if the customer exists
        check_query = text("SELECT * FROM customer WHERE customer_id = :customer_id")
        result = db.session.execute(check_query, {"customer_id": customer_id}).fetchone()

        if not result:
            print(f"❌ Customer ID {customer_id} not found!")
            return jsonify({"error": "Customer not found"}), 404

        print(f"✅ Customer ID {customer_id} exists. Checking related rentals...")

        # Step 2️⃣: Check if customer has related rentals
        check_rentals_query = text("SELECT * FROM rental WHERE customer_id = :customer_id")
        rental_result = db.session.execute(check_rentals_query, {"customer_id": customer_id}).fetchone()

        if rental_result:
            print(f"❗ Customer has related rentals. Deleting rentals first...")
            delete_rentals_query = text("DELETE FROM rental WHERE customer_id = :customer_id")
            db.session.execute(delete_rentals_query, {"customer_id": customer_id})
            db.session.commit()
            print(f"🗑 Deleted related rentals.")

        # Step 3️⃣: Now delete the customer
        print(f"🗑 Deleting customer...")
        delete_query = text("DELETE FROM customer WHERE customer_id = :customer_id")
        db.session.execute(delete_query, {"customer_id": customer_id})
        db.session.commit()

        print(f"✅ Customer ID {customer_id} deleted successfully!")
        return jsonify({"message": f"Customer ID {customer_id} deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"❗ ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500



@customers_bp.route('/customers/<int:customer_id>/rentals', methods=['GET'])
def get_customer_rental_history(customer_id):
    try:
        # Query to get rental history for a customer
        query = text("""
            SELECT 
                r.rental_id, 
                r.rental_date, 
                r.return_date,
                f.title AS movie_title,
                r.staff_id
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            WHERE r.customer_id = :customer_id
            ORDER BY r.rental_date DESC
        """)

        result = db.session.execute(query, {"customer_id": customer_id}).fetchall()

        if not result:
            return jsonify({"message": "No rental history found for this customer"}), 404

        rental_history = [
            {
                "rental_id": row.rental_id,
                "rental_date": row.rental_date.strftime("%Y-%m-%d"),
                "return_date": row.return_date.strftime("%Y-%m-%d") if row.return_date else "Not Returned",
                "movie_title": row.movie_title,
                "staff_id": row.staff_id
            }
            for row in result
        ]

        return jsonify({"customer_id": customer_id, "rental_history": rental_history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500