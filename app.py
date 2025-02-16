from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "working"

csv_file = os.path.join(os.getcwd(), "public", "movie.csv")


# movie 
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify([
        {
            "name": "BUCKET BROTHERHOOD",
            "genre": "Description: A Amazing Display of a Girl And a Womanizer who must Succumb a "
                    "Lumberjack in A Baloon Factory\n"
                    "Release: 2006\n"
                    "Rental Count: 34\n"
                    "Rental Rate: 4.99",
            "image": "/public/11.jpg"
        },
        {
            "name": "ROCKETEER MOTHER",
            "genre": "A Awe-Inspiring Character Study of a Robot And a Sumo Wrestler "
                    "who must Discover a Womanizer in A Shark Tank\n"
                    "Release: 2006\n"
                    "Rental Count: 33\n"
                    "Rental Rate: 0.99",
            "image": "/public/11.jpg"
        },
        {
            "name": "FORWARD TEMPLE",
            "genre": "A astounding display of a forensic psychologist and a mad scientist who"
                    "must challenge a girl in New Orleans \n"
                    "Release: 2006\n"
                    "Rental Count: 32\n"
                    "Rental Rate: 2.99",
            "image": "/public/11.jpg"
        },
        {
            "name": "JUGGLER HARDLY",
            "genre": "A Epic Story of a Mad Cow And a Astronaut "
                    "who must Challenge a Car in California\n"
                    "Release: 2006\n"
                    "Rental Count: 32\n"
                    "Rental Rate: 0.99",
            "image": "/public/11.jpg"
        },
        {
            "name": "GRIT CLOCKWORK",
            "genre": "A thoughtful display of a dentist and a squirrel who must confront a lumberjack"
                    "in a shark tank\n"
                    "Release: 2006\n"
                    "Rental Count: 32\n"
                    "Rental Rate: 0.99",
            "image": "/public/11.jpg"
        }
    ])



#actor  
@app.route('/api/actors', methods=['GET'])
def get_actors():
    return jsonify([
        {
              "name": "GINA DEGRENERES",
        "description": "Top 5 Movies:\n1:GOODFELLAS SALUTE\n2:WIFE TURN\n3:DEER VIRGINIAN\n4:GODMA FAMILY\n5:STORM HAPPINESS",
            "image": "/public/6.jpg"
        },
        {
            "name": "MARY KEITEL",
            "description": "Top 5 Movies:\n1:BUTTERFLY CHOCOLAT\n2:IDOLS SNATCHERS\n3:ROSES TREASURE\n4:HANDICAP BOONDOCK\n5:FANTASY TROOPERS",
            "image": "/public/5.jpg"
        },
        {
            "name": "WALTER TORN",
            "description": "Top 5 Moivess:\n1:HOBBIT ALIEN\n2:WITCHES PANIC\n3:WARDROBE PHANTOM\n4:CURTAIN VIDEOTAPE\n5:LIES TREATMENT",
            "image": "/public/4.jpg"
        },
        {
            "name": "MATTHEW CARREY",
            "description": "Top 5 Moives:\n1:HARRY IDAHO\n2:MUSCLE BRIGHT\n3:FAMILY SWEET\n4:TRIP NEWTON\n5:NONE SPIKING",
            "image": "/public/3.jpg"
        },
        {
            "name": "SANDRA KILMER",
            "description": "Top 5 Moives:\n1:BLACKOUT PRIVATE\n2:GOLDMINE TYCOON\n3:STREETCAR INTENTIONS\n4:SLEEPING SUSPECTS\n5:JUMPING WRATH",
            "image": "/public/2.jpg"
        }
    ])


@app.route("/api/table", methods=["GET"])
def get_table():
    try:
        if not os.path.exists(csv_file):
            return jsonify({"error": "CSV can't find it"}), 404

        df = pd.read_csv(csv_file)
        df.fillna("", inplace=True)

       
        grouped = df.groupby("film_id").agg({
            "title": "first",
            "description": "first",
            "release_year": "first",
            "rating": "first",
            "length": "first",
            "rental_duration": "first",
            "rental_rate": "first",
            "replacement_cost": "first",
            "special_features": "first",
            "actor_id": list,
            "first_name": list,
            "last_name": list
        }).reset_index()

        
        grouped["actors"] = grouped.apply(
            lambda row: [f"{fn} {ln}" for fn, ln in zip(row["first_name"], row["last_name"])], axis=1
        )

        
        grouped.drop(columns=["first_name", "last_name", "actor_id"], inplace=True)

        result = grouped.to_dict(orient="records")

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/customers", methods=["GET"])
def get_customers():
    try:
        customer_file = os.path.join(os.getcwd(), "public", "customerdetail.csv")  # ✅ 确保路径正确
        if not os.path.exists(customer_file):
            return jsonify({"error": "Customer 数据文件未找到"}), 404

        df = pd.read_csv(customer_file)
        df.fillna("", inplace=True)

        customers = df.to_dict(orient="records")  # 🔥 转换为 JSON 数组
        return jsonify(customers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
