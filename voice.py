# -*- coding: utf-8 -*-
"""
ജാതകംGPT — Natural Indian Malayali Astrologer Voice Generation Module
Character: Brahmasree Biju (Voice: ml-IN-MidhunNeural)
Tuned with authentic Kerala astrologer cadence, theatrical pauses, and resonant tone.
"""
import os
import hashlib
import edge_tts

AUDIO_CACHE_DIR = os.path.join(os.path.dirname(__file__), "static", "audio_cache")
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

VOICE_NAME = "ml-IN-MidhunNeural"
VOICE_RATE = "-3%"    # Crisp, natural conversational cadence with dramatic gravity
VOICE_PITCH = "-1Hz"  # Authoritative, resonant, experienced astrologer tone

async def get_or_create_audio(text: str, filename_prefix: str = "biju") -> str:
    """
    Generate or retrieve cached MP3 file for given Malayalam speech text.
    Returns relative URL path for client playback.
    """
    cleaned_text = text.strip()
    text_hash = hashlib.md5(cleaned_text.encode("utf-8")).hexdigest()
    filename = f"{filename_prefix}_{text_hash}.mp3"
    filepath = os.path.join(AUDIO_CACHE_DIR, filename)

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        communicate = edge_tts.Communicate(
            text=cleaned_text,
            voice=VOICE_NAME,
            rate=VOICE_RATE,
            pitch=VOICE_PITCH
        )
        await communicate.save(filepath)

    return f"/static/audio_cache/{filename}"

async def save_direct_audio(text: str, filename: str) -> str:
    """
    Generate and save an audio file with an exact filename (used for scanning audio clips).
    """
    filepath = os.path.join(AUDIO_CACHE_DIR, filename)
    communicate = edge_tts.Communicate(
        text=text.strip(),
        voice=VOICE_NAME,
        rate=VOICE_RATE,
        pitch=VOICE_PITCH
    )
    await communicate.save(filepath)
    return f"/static/audio_cache/{filename}"
