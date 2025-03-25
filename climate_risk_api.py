from fastapi import FastAPI
import requests
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
API_KEY = os.getenv("API_KEY")
print("API KEY:", API_KEY)
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# === Load flood-prone district data ===
flood_df = pd.read_csv("data/flood_prone_districts.csv")

# === FastAPI app ===
app = FastAPI()

# === Home Route ===
@app.get("/")
def home():
    return {"message": "Welcome to India's Climate Risk API!"}

# === Weather Fetch Function ===
def get_weather_data(district):
    params = {
        "q": f"{district},IN",
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "main" not in data or "weather" not in data:
            return {"error": "Invalid API response"}

        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except:
        return {"error": "District not found or API issue"}

# === Flood Risk Function ===
def get_flood_risk(district_name):
    row = flood_df[flood_df["district"].str.lower() == district_name.lower()]
    if not row.empty:
        return row.iloc[0]["flood_prone_level"]
    return "Unknown"

# === Main Route: Climate Risk API ===
@app.get("/climate-risk/{district}")
def get_climate_risk(district: str):
    weather_data = get_weather_data(district)

    if "error" in weather_data:
        return {"error": "District not found or API issue"}

    flood_risk = get_flood_risk(district)

    return {
        "district": district,
        "weather": weather_data,
        "flood_risk_level": flood_risk
    }
