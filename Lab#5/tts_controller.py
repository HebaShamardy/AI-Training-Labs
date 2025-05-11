from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from tts_service import TextToSpeechService
import io

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: str

@router.post("/tts")
def generate_voice(data: TTSRequest):
    tts = TextToSpeechService()
    audio_content = tts.synthesize_text(data.text, data.language)
    return StreamingResponse(io.BytesIO(audio_content), media_type="audio/mp3")

