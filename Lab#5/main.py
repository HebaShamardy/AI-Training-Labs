from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import uvicorn
from mongodb import connect_to_mongo, close_mongo_connection
from discovery_client import connect_discovery
from stt_service import SpeechToTextService
from tts_service import TextToSpeechService
import products_controller
import reviews_controller
import stt_controller
import tts_controller
import watson_discovery_controller
from dotenv import load_dotenv
import yaml

load_dotenv()  # This loads the .env file into os.environ

def read_config():
    with open("config.yml") as f:
        app.state.config = yaml.safe_load(f)

def connect_stt():
    SpeechToTextService.connect_stt()
    print("STT service initialized.")

def connect_tts():
    TextToSpeechService.connect_tts()
    print("TTS service initialized.")

SEARCH_API_URL = os.environ.get("SEARCH_API_URL")
API_KEY = os.environ.get("API_KEY")  

class SearchQuery(BaseModel):
 search_engine: Optional[str] = "google"
 query: str

app = FastAPI()

# include the product router
app.include_router(products_controller.router)
app.include_router(reviews_controller.router)
app.include_router(watson_discovery_controller.router)
app.include_router(stt_controller.router)
app.include_router(tts_controller.router)

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
    

#Add startup and shutdown events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("startup", read_config)
app.add_event_handler("startup", connect_stt)
app.add_event_handler("startup", connect_tts)
app.add_event_handler("startup", connect_discovery)
app.add_event_handler("shutdown", close_mongo_connection)

if __name__ == "__main__":
    # Use the environment variable for the port, default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)