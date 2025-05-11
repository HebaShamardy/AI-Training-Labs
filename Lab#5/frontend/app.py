import streamlit as st
import sounddevice as sd
import soundfile as sf
import asyncio
import websockets
import json
import tempfile
import requests

st.title("🗣️ Multilingual Voice Chatbot")

lang = st.selectbox("Choose Language", ["english", "arabic"])
transcript_holder = st.empty()

async def send_audio(audio_data, lang):
    uri = "ws://localhost:8000/ws/stt"
    try:
        async with websockets.connect(uri, max_size=None) as websocket:
            await websocket.send(json.dumps({"language": lang}))
            await websocket.send(audio_data)
            response = await websocket.recv()
            resp_json = json.loads(response)
            transcript=resp_json['transcript']
            transcript_holder.success(f"Transcript: {transcript}")
            
            # 🔁 Now call TTS to get voice for transcript
            tts_resp = requests.post("http://localhost:8000/tts", json={
                "text": transcript,
                "language": lang
            })

            # 🔊 Play audio
            if tts_resp.ok:
                audio_bytes = tts_resp.content
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Failed to generate TTS audio.")
    except Exception as e:
        transcript_holder.error(f"Error: {e}")

if st.button("🎤 Speak"):
    duration = 10  # seconds
    samplerate = 44100
    st.info("Recording...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio, samplerate)
        with open(tmp.name, "rb") as f:
            audio_data = f.read()

    asyncio.run(send_audio(audio_data, lang))
