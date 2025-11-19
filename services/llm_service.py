import os
import requests
from typing import List

GROQ_API_KEY = os.getenv('GROQ_API_KEY','')
GROQ_ENDPOINT = os.getenv('GROQ_ENDPOINT','https://api.groq.com/v1')

def _template_generate_captions(topic: str, n_lines: int = 5) -> List[str]:
    base = topic
    if ':' in base:
        base = base.split(':',1)[1].strip()
    parts = [
        base if len(base) <= 40 else base[:40].rstrip() + '...',
        'Did you know? ' + (base if len(base) <= 30 else base[:30].rstrip() + '...'),
        'Quick fact: ' + (base if len(base) <= 28 else base[:28].rstrip() + '...'),
        'True and surprising',
        'Follow for more facts!'
    ]
    return parts[:n_lines]

def generate_captions(topic: str, n_lines: int = 5) -> List[str]:
    if not GROQ_API_KEY:
        return _template_generate_captions(topic, n_lines)
    try:
        prompt = f"Generate {n_lines} concise captions (4-8 words each) for a YouTube short about: {topic}. Return as a JSON array of strings."
        headers = {'Authorization': f'Bearer {GROQ_API_KEY}','Content-Type':'application/json'}
        data = {'model':'llama3-mini','input':prompt,'max_output_tokens':300}
        resp = requests.post(f'{GROQ_ENDPOINT}/invoke', headers=headers, json=data, timeout=15)
        resp.raise_for_status()
        j = resp.json()
        # parse conservatively
        text = ''
        if isinstance(j, dict):
            text = j.get('output') or j.get('text') or j.get('result') or ''
            if isinstance(text, list):
                return [str(x).strip() for x in text][:n_lines]
            text = str(text)
        else:
            text = str(j)
        lines = [l.strip('-•* \t') for l in text.splitlines() if l.strip()]
        if lines:
            return lines[:n_lines]
        import json
        try:
            arr = json.loads(text)
            if isinstance(arr, list):
                return [str(x) for x in arr][:n_lines]
        except Exception:
            pass
        return _template_generate_captions(topic, n_lines)
    except Exception:
        return _template_generate_captions(topic, n_lines)
