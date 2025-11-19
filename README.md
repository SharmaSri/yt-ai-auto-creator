"""
# YT-AI-Auto-Creator — Facts Shorts (Quotes on Screen)


This project automates creation of YouTube Shorts (30 second) showing
quotes/facts on-screen. It's free-only (no paid APIs required).


Niche: Facts
Format: 30 second Shorts (vertical 1080x1920) with quotes on screen.
Style: Quotes on screen only (no narration).


## Features
- Topic/Quote selection agent (pulls from local dataset + web scraping)
- Script writer agent (converts facts into short captions)
- Video editor agent (creates 30s vertical video, text slides + background music)
- Thumbnail agent (creates simple thumbnail)
- Upload agent (YouTube API - optional; run dry-run without keys)


## Requirements
Python 3.11.9
Install dependencies:


```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# mac/linux
source .venv/bin/activate
pip install -r requirements.txt
```


## Quick run (dry-run)
1. Create `.env` from `.env.example` and leave blank or add YOUTUBE credentials if you will upload.
2. Place any optional assets (music) in `assets/background_music/`.
3. Run:


```bash
python main.py --dry-run
```


Output video will be in `outputs/videos/` as a 30 second vertical MP4.


## Notes
- This project is designed for Shorts (vertical 9:16). For landscape change dimensions in `video_editing_agent.py`.
- YouTube upload requires creating `client_secret.json` and OAuth consent – skip upload for now.
"""