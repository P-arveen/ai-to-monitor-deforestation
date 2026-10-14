from flask import Flask, jsonify
import requests
from collections import defaultdict

app = Flask(__name__)

# 10 major Indian cities with coordinates
india_locations = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Lucknow": (26.8467, 80.9462),
    "Guwahati": (26.1445, 91.7362),
    "Bhopal": (23.2599, 77.4126)
}

def fetch_avg_temp(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean",
        "timezone": "UTC"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "daily" not in data or "temperature_2m_mean" not in data["daily"]:
        raise ValueError("Missing temperature data")
    temps = [t for t in data["daily"]["temperature_2m_mean"] if t is not None]
    return sum(temps) / len(temps) if temps else None

def get_year_avg(year):
    start = f"{year}-01-01"
    end = f"{year}-12-31"
    city_averages = []

    for city, (lat, lon) in india_locations.items():
        try:
            avg_temp = fetch_avg_temp(lat, lon, start, end)
            if avg_temp is not None:
                city_averages.append(avg_temp)
        except Exception as e:
            print(f"Failed to fetch data for {city} ({year}):", e)

    return sum(city_averages) / len(city_averages) if city_averages else 0

