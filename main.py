from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,         # Whether to allow cookies/auth headers
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)

POKEMON_JSON_PATH = os.path.join(os.path.dirname(__file__), "pokemon_data.json")
POKEMON_API_URL = "http://localhost:8000/pokemon"

class Patient(BaseModel):
    id: int
    name: str
    birth_date: date
    email: Optional[str] = None

# Simulated in-memory database
patients_db: List[Patient] = []

@app.get("/pokemon")
def get_pokemon(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1)
):
    # Load data from JSON file
    with open(POKEMON_JSON_PATH, "r") as f:
        data = json.load(f)
    all_results = data
    count = data.__len__()

    # Paginate results
    paginated = all_results[offset:offset+limit]

    # Build next and previous URLs
    next_offset = offset + limit
    prev_offset = offset - limit if offset - limit >= 0 else 0

    next_url = (
        f"{POKEMON_API_URL}?offset={next_offset}&limit={limit}"
        if next_offset < count else None
    )
    previous_url = (
        f"{POKEMON_API_URL}?offset={prev_offset}&limit={limit}"
        if offset > 0 else None
    )

    return {
        "count": count,
        "next": next_url,
        "previous": previous_url,
        "results": paginated
    }

@app.get("/pokemon/{pokemon_id}/")
def get_pokemon_detail(pokemon_id: int):
    detail_json_path = os.path.join(os.path.dirname(__file__), "pokemon_detail_data.json")
    try:
        with open(detail_json_path, "r") as f:
            details = json.load(f)
        # pokemon_id is 1-based, so index is pokemon_id - 1
        index = pokemon_id - 1
        if index < 0 or index > len(details):
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return details[index]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
