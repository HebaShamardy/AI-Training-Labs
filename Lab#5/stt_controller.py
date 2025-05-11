from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from pydantic import BaseModel
from stt_service import SpeechToTextService
import json
import logging
import uuid
import os

router = APIRouter()

class STTRequest(BaseModel):
    language: str

@router.websocket("/ws/stt")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        json_msg = await websocket.receive_text()
        stt_request = STTRequest(**json.loads(json_msg))
        audio = await websocket.receive_bytes()
        # 💾 Save audio to file
        # filename = f"{uuid.uuid4().hex}.wav"
        # save_path = os.path.join("audio_uploads", filename)
        # os.makedirs("audio_uploads", exist_ok=True)
        # with open(save_path, "wb") as f:
        #     f.write(audio)
        # print(f"Saved audio to {save_path}")
        
        print(f"Received audio for language: {stt_request.language}")
        
        # Actual transcription can be done here:
        config = websocket.app.state.config
        stt_service = SpeechToTextService()
        transcript = stt_service.transcribe_audio(stt_request.language, audio, config)
        # transcript = "This is a fake transcript for testing."

        await websocket.send_json({"transcript": transcript})
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        logging.exception("WebSocket error")
        await websocket.close()
