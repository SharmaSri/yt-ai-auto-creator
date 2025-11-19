"""
VideoEditorAgent — creates a vertical 1080x1920, 30s video.
- Displays each caption as a full-screen slide for equal intervals.
- Optionally overlays a background music track if present in assets.
- Works on Windows without ImageMagick (uses PIL + ImageClip).
"""
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, afx
from PIL import Image, ImageDraw, ImageFont
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_DURATION_SECONDS, FPS, BG_MUSIC_DIR, OUTPUT_DIR
from utils.file_manager import ensure_dirs
from utils.time_utils import timestamp_now

ensure_dirs()  # make sure OUTPUT_DIR/videos exists

class VideoEditorAgent:
    def __init__(self, font_path: str = "C:\\Windows\\Fonts\\arial.ttf"):
        """
        :param font_path: Full path to a TrueType font file (Windows example: arial.ttf)
        """
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found at {font_path}. Provide a valid TTF font path.")
        self.font_path = font_path

    def create_image_clip(self, text: str, duration: float) -> ImageClip:
        """
        Create a single ImageClip with text centered on a background.
        """
        # Create black background image
        img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(18, 18, 18))
        draw = ImageDraw.Draw(img)

        # Load font
        font_size = 90
        font = ImageFont.truetype(self.font_path, font_size)

        # Wrap text if too long (simple word wrap)
        max_width = VIDEO_WIDTH - 120
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Compute total text height for vertical centering
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_heights.append(bbox[3] - bbox[1])
        total_text_height = sum(line_heights) + (len(lines) - 1) * font_size * 0.2

        y = (VIDEO_HEIGHT - total_text_height) / 2
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (VIDEO_WIDTH - w) / 2
            draw.text((x, y), line, font=font, fill="white")
            y += h * 1.2  # line spacing

        # Save temporary image
        temp_path = os.path.join(OUTPUT_DIR, "temp_slide.png")
        img.save(temp_path)

        # Load as ImageClip
        clip = ImageClip(temp_path).set_duration(duration)
        return clip

    def create_video(self, captions: list, audio_path: str | None = None) -> str:
        """
        Create a vertical video from a list of captions.
        :param captions: list of strings to display
        :param audio_path: optional path to background audio
        :return: output video path
        """
        n = max(1, len(captions))
        per = VIDEO_DURATION_SECONDS / n

        clips = [self.create_image_clip(caption, per) for caption in captions]

        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")

        # Attach provided audio if available
        if audio_path and os.path.exists(audio_path):
            try:
                bg_audio = AudioFileClip(audio_path).fx(afx.audio_loop, duration=VIDEO_DURATION_SECONDS)
                final_video = final_video.set_audio(bg_audio)
            except Exception as e:
                print("Warning: failed to attach provided audio:", e)

        # Otherwise use first available default background music
        elif os.path.exists(BG_MUSIC_DIR):
            try:
                music_files = [f for f in os.listdir(BG_MUSIC_DIR) if f.endswith((".mp3", ".wav"))]
                if music_files:
                    music_path = os.path.join(BG_MUSIC_DIR, music_files[0])
                    bg_music = AudioFileClip(music_path).fx(afx.audio_loop, duration=VIDEO_DURATION_SECONDS).volumex(0.25)
                    final_video = final_video.set_audio(bg_music)
            except Exception as e:
                print("Warning: failed to attach default background music:", e)

        # Export final video
        out_path = os.path.join(OUTPUT_DIR, "videos", f"short_{timestamp_now()}.mp4")
        final_video.write_videofile(
            out_path,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="medium"
        )

        return out_path
