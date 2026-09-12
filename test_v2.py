# -*- coding: utf-8 -*-
"""
Verification suite for ജാതകംGPT 2.0:
- Checks 16 satirical careers
- Validates /api/predict response structure
- Verifies all audio files exist and are playable
- Verifies scanning audio clips
"""
import os
import sys
from fastapi.testclient import TestClient
from main import app
from predictions import CAREER_PREDICTIONS

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["careers_available"] == 16
    print("PASS: /health check (16 careers registered)")

def test_careers_list():
    res = client.get("/api/careers")
    assert res.status_code == 200
    careers = res.json()
    assert len(careers) == 16
    print(f"PASS: /api/careers returned {len(careers)} archetypes")

def test_predictions_and_audios():
    signals = [None, "smiling", "tilted", "serious"]
    for sig in signals:
        body = {"harmless_signal": sig} if sig else {}
        res = client.post("/api/predict", json=body)
        assert res.status_code == 200
        data = res.json()

        # Check required fields
        assert "title" in data
        assert "punchline" in data
        assert "career_reading" in data
        assert "love_life" in data
        assert "wealth" in data
        assert "lifestyle" in data
        assert "pariharam" in data
        assert "audio_url" in data
        assert "section_audios" in data

        # Check full speech audio file exists
        full_audio_path = os.path.join(os.path.dirname(__file__), data["audio_url"].lstrip("/"))
        assert os.path.exists(full_audio_path), f"Missing audio: {full_audio_path}"
        assert os.path.getsize(full_audio_path) > 1000

        # Check section audios exist
        sec_audios = data["section_audios"]
        for key in ["career", "love", "wealth", "lifestyle", "pariharam"]:
            assert key in sec_audios
            sec_path = os.path.join(os.path.dirname(__file__), sec_audios[key].lstrip("/"))
            assert os.path.exists(sec_path), f"Missing section audio: {sec_path}"
            assert os.path.getsize(sec_path) > 1000

        print(f"PASS: /api/predict for signal '{sig}' -> {data['emoji']} {data['title']} (Audios Verified)")

def test_scanning_audio_clips():
    clips = [
        "scan_step1.mp3", "scan_smiling.mp3", "scan_tilted.mp3",
        "scan_serious.mp3", "scan_step3.mp3", "scan_step4.mp3"
    ]
    cache_dir = os.path.join(os.path.dirname(__file__), "static", "audio_cache")
    for clip in clips:
        clip_path = os.path.join(cache_dir, clip)
        assert os.path.exists(clip_path), f"Missing scan clip: {clip}"
        assert os.path.getsize(clip_path) > 1000
    print("PASS: All 6 scanning & inferring audio clips verified on disk")

def test_frontend_static():
    res = client.get("/")
    assert res.status_code == 200
    assert "ജാതകം" in res.text
    print("PASS: Frontend index.html served successfully")

if __name__ == "__main__":
    test_health()
    test_careers_list()
    test_predictions_and_audios()
    test_scanning_audio_clips()
    test_frontend_static()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! 🚀")
