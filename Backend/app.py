from flask import Flask, request, jsonify
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Replace this with your actual OpenWeatherMap API key
API_KEY = "a4ea97f73062de8ba2c2afd3bb51bef3"

# Initialize the database
def init_db():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            date_range TEXT NOT NULL,
            weather_info TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return """
    <h1>Welcome to the Weather App</h1>
    <p>Use the following endpoints:</p>
    <ul>
        <li>Current Weather: <a href="/weather?location=Seattle">/weather?location=Seattle</a></li>
        <li>5-Day Forecast: <a href="/forecast?location=Seattle">/forecast?location=Seattle</a></li>
        <li>CRUD Operations: Use /save-weather, /get-weather-data, /update-weather/<id>, and /delete-weather/<id></li>
    </ul>
    """

@app.route("/weather", methods=["GET"])
def get_weather():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch weather data"}), 500

    data = response.json()

    # Format the response
    formatted_data = {
        "location": data.get("name"),
        "temperature": data["main"].get("temp"),
        "description": data["weather"][0].get("description"),
        "humidity": data["main"].get("humidity"),
        "pressure": data["main"].get("pressure"),
        "wind_speed": data["wind"].get("speed"),
        "country": data["sys"].get("country"),
    }

    return jsonify(formatted_data)

@app.route("/forecast", methods=["GET"])
def get_forecast():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch forecast data"}), 500

    data = response.json()

    # Simplify the 5-day forecast data
    forecast_data = []
    for entry in data["list"]:
        forecast_data.append({
            "datetime": entry["dt_txt"],
            "temperature": entry["main"]["temp"],
            "description": entry["weather"][0]["description"],
        })

    return jsonify({"location": data["city"]["name"], "country": data["city"]["country"], "forecast": forecast_data})

# CRUD Operations
@app.route("/save-weather", methods=["POST"])
def save_weather():
    data = request.json
    location = data.get("location")
    date_range = data.get("date_range")
    weather_info = data.get("weather_info")

    if not location or not date_range or not weather_info:
        return jsonify({"error": "Location, date_range, and weather_info are required"}), 400

    try:
        datetime.strptime(date_range, "%Y-%m-%d to %Y-%m-%d")  # Validate date range format
    except ValueError:
        return jsonify({"error": "Invalid date_range format. Use 'YYYY-MM-DD to YYYY-MM-DD'"}), 400

    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("INSERT INTO weather_data (location, date_range, weather_info) VALUES (?, ?, ?)",
              (location, date_range, weather_info))
    conn.commit()
    conn.close()

    return jsonify({"message": "Weather data saved successfully"}), 201

@app.route("/get-weather-data", methods=["GET"])
def get_weather_data():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT * FROM weather_data")
    rows = c.fetchall()
    conn.close()

    results = [{"id": row[0], "location": row[1], "date_range": row[2], "weather_info": row[3]} for row in rows]

    return jsonify(results)

@app.route("/update-weather/<int:id>", methods=["PUT"])
def update_weather(id):
    data = request.json
    weather_info = data.get("weather_info")

    if not weather_info:
        return jsonify({"error": "weather_info is required"}), 400

    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("UPDATE weather_data SET weather_info = ? WHERE id = ?", (weather_info, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Weather data updated successfully"}), 200

@app.route("/delete-weather/<int:id>", methods=["DELETE"])
def delete_weather(id):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("DELETE FROM weather_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Weather data deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
