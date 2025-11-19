"""
ThumbnailAgent — creates a simple thumbnail using Pillow (landscape 1280x720).
For Shorts, thumbnails are optional but created anyway for YouTube Studio.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from utils.time_utils import timestamp_now
from config import OUTPUT_DIR

class ThumbnailAgent:
    def __init__(self):
        pass

    def create_thumbnail(self, captions:list, topic:str) -> str:
        W, H = 1280, 720
        img = Image.new('RGB', (W,H), color=(30,30,30))
        draw = ImageDraw.Draw(img)
        title = captions[0] if captions else (topic[:60]+'...')
        try:
            font = ImageFont.truetype('arial.ttf', 60)
        except Exception:
            font = ImageFont.load_default()
        draw.text((40, H//2 - 30), title, fill=(255,255,255), font=font)
        outp = os.path.join(OUTPUT_DIR, 'thumbnails', f'thumb_{timestamp_now()}.png')
        os.makedirs(os.path.dirname(outp), exist_ok=True)
        img.save(outp)
        return outp