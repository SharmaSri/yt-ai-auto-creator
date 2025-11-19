import os
from pathlib import Path
from gtts import gTTS
import requests

TTSMAKER_KEY = os.getenv('TTSMAKER_API_KEY','')
OUTPUT_AUDIO_DIR = Path(os.getenv('OUTPUT_DIR','./outputs')) / 'audio'
OUTPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def ttsmaker_synthesize(text: str, voice: str = 'v4') -> Path:
    """Call TTSMaker API if key present. Returns Path to mp3."""
    if not TTSMAKER_KEY:
        raise RuntimeError('TTSMAKER_API_KEY not configured')
    url = 'https://api.ttsmaker.com/synthesize'
    headers = {'Authorization': f'Bearer {TTSMAKER_KEY}'}
    payload = {'voice': voice, 'text': text}
    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    audio_url = data.get('audio_url') or data.get('url')
    if not audio_url:
        raise RuntimeError('No audio URL from TTSMaker')
    r = requests.get(audio_url, timeout=30)
    fname = OUTPUT_AUDIO_DIR / f'tts_{int(__import__("time").time())}.mp3'
    with open(fname, 'wb') as f:
        f.write(r.content)
    return fname

def gtts_synthesize(text: str, lang: str = 'en') -> Path:
    fname = OUTPUT_AUDIO_DIR / f'gtts_{int(__import__("time").time())}.mp3'
    tts = gTTS(text=text, lang=lang)
    tts.save(str(fname))
    return fname

def synthesize(text: str, prefer: str = 'v4') -> Path:
    """Try TTSMaker first if configured, else fallback to gTTS."""
    try:
        if TTSMAKER_KEY:
            return ttsmaker_synthesize(text, voice=prefer)
    except Exception:
        pass
    return gtts_synthesize(text)
