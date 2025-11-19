import os

OUTPUT_DIR = os.getenv('OUTPUT_DIR','./outputs')
VIDEO_DURATION_SECONDS = 30  # target duration for shorts
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24

# Paths
ASSETS_DIR = os.path.join(os.getcwd(),'assets')
STOCK_VIDEOS_DIR = os.path.join(ASSETS_DIR,'stock_videos')
BG_MUSIC_DIR = os.path.join(ASSETS_DIR,'background_music')