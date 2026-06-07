from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Wonderful Places API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PLACES = {
    "17.4062,78.4691": {
        "name": "Birla Mandir",
        "distance": "4 km",
        "duration": "10 mins",
        "location": "Hill Fort Road, Hyderabad"
    },
    "17.3833,78.4011": {
        "name": "Golconda Fort",
        "distance": "12 km",
        "duration": "28 mins",
        "location": "Khair Complex, Hyderabad"
    },
    "17.2543,78.6808": {
        "name": "Ramoji Film City",
        "distance": "35 km",
        "duration": "50 mins",
        "location": "Abdullapurmet, Hyderabad"
    },
    "17.3616,78.4747": {
        "name": "Charminar",
        "distance": "5 km",
        "duration": "15 mins",
        "location": "Old City, Hyderabad"
    },
    "17.4239,78.4738": {
        "name": "Hussain Sagar",
        "distance": "6 km",
        "duration": "18 mins",
        "location": "Tank Bund, Hyderabad"
    }
}


@app.get("/")
def home():
    return {
        "message": "Wonderful Places API Running"
    }


@app.get("/route")
def get_route(dest_lat: float, dest_lng: float):

    key = f"{dest_lat},{dest_lng}"

    if key not in PLACES:
        return {
            "error": "Location not found"
        }

    place = PLACES[key]

    return {
    "place_name": place["name"],
    "distance": place["distance"],
    "duration": place["duration"],
    "location": place["location"],
    
}