from flask import Flask, jsonify, request
import datetime
import os
import pandas as pd

app = Flask(__name__)

@app.route('/date', methods=['GET'])
def get_date():
    now = datetime.datetime.now()
    return jsonify({'date': now.strftime("%Y-%m-%d")})

@app.route('/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    if not data or "location" not in data:
        return jsonify({"error": "Please provide a location in the request body"}), 400

    location_requested = data["location"].strip().lower()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    recipes_csv = os.path.join(base_dir, "recipes.csv")
    
    try:
        recipes_df = pd.read_csv(recipes_csv)
        filtered_df = recipes_df[recipes_df["Location"].str.lower().str.strip() == location_requested]
        recipes = filtered_df.to_dict(orient="records")
        return jsonify(recipes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/plants', methods=['POST'])
def get_plants():
    data = request.get_json()
    if not data or "location" not in data:
        return jsonify({"error": "Please provide a location in the request body"}), 400

    location_requested = data["location"].strip().lower()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    weather_csv = os.path.join(base_dir, "dataset_weather.csv")
    plants_csv = os.path.join(base_dir, "cleanData.csv")
    
    try:
        weather_df = pd.read_csv(weather_csv)
        weather_filtered = weather_df[weather_df["Location"].str.lower().str.strip() == location_requested]
        if not weather_filtered.empty:
            avg_temp = weather_filtered["AirTemperatureCelsius"].mean()
        else:
            avg_temp = None

        plants_df = pd.read_csv(plants_csv)
        plants_filtered = plants_df[plants_df["Location"].str.lower().str.strip() == location_requested]
        if not plants_filtered.empty:
            plants_str = plants_filtered.iloc[0]["Plants"]
            possible_plants = [plant.strip() for plant in plants_str.split(';') if plant.strip() != ""]
        else:
            possible_plants = []

        response = {
            "location": data["location"],
            "temperature": avg_temp,
            "possible_plants": possible_plants
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/plantInfo', methods=['POST'])
def get_plant_info():
    data = request.get_json()
    if not data or "plant" not in data:
        return jsonify({"error": "Please provide a plant name in the request body"}), 400

    plant_requested = data["plant"].strip().lower()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data'))
    edible_csv = os.path.join(base_dir, "dataset_edible_plants.csv")
    
    try:
        edible_df = pd.read_csv(edible_csv)
        filtered_df = edible_df[edible_df["Name"].str.lower().str.strip() == plant_requested]
        if filtered_df.empty:
            return jsonify({"error": f"No info found for plant: {data['plant']}"}), 404
        plant_info = filtered_df.to_dict(orient="records")
        return jsonify(plant_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run()