from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

SEARCH_API_URL = "https://www.searchapi.io/api/v1/search"
API_KEY = "<search_api_key>" # use it only local, don't push it anywhere


class SearchQuery(BaseModel):
 search_engine: Optional[str] = "google"
 query: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.post("/search/")
def search_google(search_query: SearchQuery):
    params = {
        "api_key": API_KEY,
        "engine": search_query.search_engine,
        "q": search_query.query,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "*/*"
    }
    try:
        with httpx.Client() as client:
            response = client.get(SEARCH_API_URL, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"SearchAPI Error: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to SearchAPI: {e}")
    
