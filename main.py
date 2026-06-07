from fastapi import FastAPI, Query
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Live Navigation API")

ORS_API_KEY = os.getenv("ORS_API_KEY")

START_LAT = 17.3850
START_LNG = 78.4867


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/navigate")
def navigate(dest_lat: float = Query(...), dest_lng: float = Query(...)):

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [START_LNG, START_LAT],
            [dest_lng, dest_lat]
        ]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    route = data["routes"][0]

    summary = route["summary"]
    steps = route["segments"][0]["steps"]
    geometry = route["geometry"]

    instructions = [
        {
            "instruction": step["instruction"],
            "distance": step["distance"],
            "duration": step["duration"]
        }
        for step in steps
    ]

    return {
        "distance_km": round(summary["distance"] / 1000, 2),
        "duration_min": round(summary["duration"] / 60, 2),
        "geometry": geometry,
        "instructions": instructions,
        "start": [START_LAT, START_LNG],
        "end": [dest_lat, dest_lng]
    }
