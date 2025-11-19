import os
from pathlib import Path
from config import OUTPUT_DIR


def ensure_dirs():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(OUTPUT_DIR,'audio')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(OUTPUT_DIR,'videos')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(OUTPUT_DIR,'thumbnails')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(OUTPUT_DIR,'logs')).mkdir(parents=True, exist_ok=True)