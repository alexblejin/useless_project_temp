# -*- coding: utf-8 -*-
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict

from predictions import get_prediction, CAREER_PREDICTIONS
from voice import get_or_create_audio

app = FastAPI(title="ജാതകംGPT — AI ജ്യോത്സ്യൻ")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

class PredictRequest(BaseModel):
    harmless_signal: Optional[str] = None

class VoiceRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "ജാതകംGPT",
        "character": "Brahmasree Biju",
        "careers_available": len(CAREER_PREDICTIONS)
    }

@app.post("/api/predict")
async def generate_prediction(req: Optional[PredictRequest] = None):
    signal_data = {"harmless_signal": req.harmless_signal} if req else None
    prediction = get_prediction(signal_data)

    # Generate or fetch full speech audio
    try:
        audio_url = await get_or_create_audio(prediction["full_speech"])
    except Exception as e:
        print(f"TTS warning (full speech): {e}", file=sys.stderr)
        audio_url = None

    # Generate or fetch section-specific audios for on-demand playback
    section_audios = {}
    sections_map = {
        "career": prediction.get("speech_career", prediction.get("stage3")),
        "love": prediction.get("speech_love", prediction.get("love_life")),
        "wealth": prediction.get("speech_wealth", prediction.get("wealth")),
        "lifestyle": prediction.get("speech_lifestyle", prediction.get("lifestyle")),
        "pariharam": prediction.get("speech_pariharam", prediction.get("pariharam"))
    }

    for sec_key, sec_text in sections_map.items():
        if sec_text:
            try:
                section_audios[sec_key] = await get_or_create_audio(sec_text, filename_prefix=f"sec_{sec_key}")
            except Exception as e:
                print(f"TTS warning ({sec_key}): {e}", file=sys.stderr)
                section_audios[sec_key] = None

    return {
        **prediction,
        "audio_url": audio_url,
        "section_audios": section_audios
    }

@app.post("/api/voice")
async def synthesize_voice(req: VoiceRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        audio_url = await get_or_create_audio(req.text)
        return {"audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/careers")
def list_careers():
    return [{"id": c["id"], "title": c["title"], "title_ml": c["title_ml"], "emoji": c["emoji"]} for c in CAREER_PREDICTIONS]

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ജാതകംGPT server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
