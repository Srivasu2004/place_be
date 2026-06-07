from fastapi import FastAPI, HTTPException, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hyderabad Tourist Backend API")

# ======================
# CONFIG
# ======================
ORS_API_KEY = os.getenv("ORS_API_KEY")

HYDERABAD_LAT = 17.3850
HYDERABAD_LNG = 78.4867


# ======================
# STATIC PLACES
# ======================
PLACES = [
    {"name": "Birla Mandir", "lat": 17.4062, "lng": 78.4691, "address": "Hill Fort Road, Hyderabad"},
    {"name": "Golconda Fort", "lat": 17.3833, "lng": 78.4011, "address": "Khair Complex, Hyderabad"},
    {"name": "Ramoji Film City", "lat": 17.2543, "lng": 78.6808, "address": "Abdullapurmet, Hyderabad"},
    {"name": "Charminar", "lat": 17.3616, "lng": 78.4747, "address": "Old City, Hyderabad"},
    {"name": "Hussain Sagar", "lat": 17.4239, "lng": 78.4738, "address": "Tank Bund, Hyderabad"},
]


# ======================
# ROOT
# ======================
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hyderabad Tourist API is running"
    }


# ======================
# GET ALL PLACES
# ======================
@app.get("/places")
def get_places():
    return PLACES


# ======================
# GET ROUTE DETAILS
# ======================
@app.get("/route")
def get_route(
    dest_lat: float = Query(...),
    dest_lng: float = Query(...)
):

    if not ORS_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ORS_API_KEY not found in environment"
        )

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

    try:
        response = requests.post(url, json=body, headers=headers, timeout=20)
        response.raise_for_status()

        data = response.json()

        summary = data["routes"][0]["summary"]

        distance_km = round(summary["distance"] / 1000, 2)
        duration_min = round(summary["duration"] / 60, 2)

        # match place name
        place_name = "Unknown"
        location = "Hyderabad"

        for place in PLACES:
            if abs(place["lat"] - dest_lat) < 0.001 and abs(place["lng"] - dest_lng) < 0.001:
                place_name = place["name"]
                location = place["address"]
                break

        return {
            "place_name": place_name,
            "distance": f"{distance_km} KM",
            "duration": f"{duration_min} mins",
            "location": location,
            "from": "Hyderabad",
            "to": {
                "lat": dest_lat,
                "lng": dest_lng
            }
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Route API failed: {str(e)}"
        )
