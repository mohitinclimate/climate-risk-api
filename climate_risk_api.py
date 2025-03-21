from fastapi import FastAPI
import requests
import sqlite3
import os

# Initialize FastAPI app
app = FastAPI()

# OpenWeather API Key
API_KEY = "ee0d9ea9623eb713af6bbb35dd5e5e6a"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Create database if not exists
DB_FILE = "climate_data.db"
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district TEXT,
            temperature REAL,
            humidity INTEGER,
            weather TEXT,
            wind_speed REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.get("/")
def home():
    return {"message": "Welcome to India's Climate Risk API!"}

@app.get("/climate-risk/{district}")
def get_climate_risk(district: str):
    """
    Fetch real-time weather data for a given district in India & store it in DB.
    """
    params = {
        "q": f"{district},IN",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": f"API issue: {data.get('message', 'Unknown error')}"}

        weather_info = {
            "district": district,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

        # Store in database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data (district, temperature, humidity, weather, wind_speed)
            VALUES (?, ?, ?, ?, ?)
        """, (district, weather_info["temperature"], weather_info["humidity"], weather_info["weather"], weather_info["wind_speed"]))
        conn.commit()
        conn.close()

        return weather_info

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.get("/stored-climate-data/")
def get_stored_climate_data():
    """
    Fetch all stored climate risk data from the database.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 10")  # Fetch last 10 records
        records = cursor.fetchall()
        conn.close()

        data = [
            {"id": r[0], "district": r[1], "temperature": r[2], "humidity": r[3], "weather": r[4], "wind_speed": r[5], "timestamp": r[6]}
            for r in records
        ]
        return {"stored_weather_data": data}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
