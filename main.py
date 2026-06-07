from fastapi import FastAPI, Query
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Travel + Real Route API")

ORS_API_KEY = os.getenv("ORS_API_KEY")

HYDERABAD_LAT = 17.3850
HYDERABAD_LNG = 78.4867


@app.get("/")
def home():
    return {"message": "Backend Running"}


# =========================
# REAL ROUTE API
# =========================
@app.get("/route")
def get_route(dest_lat: float = Query(...), dest_lng: float = Query(...)):

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [HYDERABAD_LNG, HYDERABAD_LAT],
            [dest_lng, dest_lat]
        ]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    route = data["routes"][0]

    summary = route["summary"]
    geometry = route["geometry"]

    return {
        "distance_km": round(summary["distance"] / 1000, 2),
        "duration_min": round(summary["duration"] / 60, 2),
        "route_geometry": geometry,   # 🔥 IMPORTANT
        "from": [HYDERABAD_LAT, HYDERABAD_LNG],
        "to": [dest_lat, dest_lng]
    }
