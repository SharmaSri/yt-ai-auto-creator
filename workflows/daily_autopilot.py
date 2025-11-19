from agents.topic_research_agent import TopicResearchAgent
from agents.script_writer_agent import ScriptWriterAgent
from agents.video_editing_agent import VideoEditorAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.voiceover_agent import VoiceoverAgent
from agents.upload_agent import UploadAgent
from utils.file_manager import ensure_dirs
from utils.logger import logger
import os

ensure_dirs()  # ensure outputs/videos and outputs/thumbnails exist

class DailyAutopilot:
    def __init__(self, upload=False):
        self.topic_agent = TopicResearchAgent()
        self.script_agent = ScriptWriterAgent()
        self.video_agent = VideoEditorAgent()
        self.thumb_agent = ThumbnailAgent()
        self.voice_agent = VoiceoverAgent()
        self.upload = upload

        if upload:
            # Use environment variable or fallback to ./client_secret.json
            client_secrets_path = os.environ.get(
                "YOUTUBE_CLIENT_SECRETS_JSON", "./client_secret.json"
            )
            if not os.path.exists(client_secrets_path):
                logger.warning(
                    f"YouTube client secrets not found at {client_secrets_path}. Upload disabled."
                )
                self.uploader = None
                self.upload = False
            else:
                self.uploader = UploadAgent(client_secrets_path=client_secrets_path)
        else:
            self.uploader = None

    def run_once(self, dry_run=True):
        topic = self.topic_agent.suggest_topic()
        logger.info(f"Selected topic: {topic}")

        # Generate script
        script_path = self.script_agent.write_script(topic)
        captions = self.script_agent.read_script_lines(script_path)

        # Generate voice audio
        audio_path = None
        try:
            audio_path = self.voice_agent.generate_voice(script_path)
            logger.info(f"Generated audio: {audio_path}")
        except Exception as e:
            logger.warning("Voice generation failed, proceeding without audio: %s", e)

        # Create video
        video_path = self.video_agent.create_video(captions, audio_path)
        logger.info(f"Created video: {video_path}")

        # Create thumbnail
        thumb_path = self.thumb_agent.create_thumbnail(captions, topic)
        logger.info(f"Created thumbnail: {thumb_path}")

        # Dry run: skip upload
        if dry_run:
            logger.info("[Dry run] Skipping upload")
            return {
                "topic": topic,
                "video": str(video_path),
                "thumbnail": str(thumb_path),
            }

        # Upload if enabled and uploader is available
        if self.upload and self.uploader:
            try:
                video_id = self.uploader.upload_video(
                    str(video_path), str(thumb_path), title=topic
                )
                logger.info(f"Uploaded video id: {video_id}")
                return {
                    "topic": topic,
                    "video": str(video_path),
                    "thumbnail": str(thumb_path),
                    "video_id": video_id,
                }
            except Exception as e:
                logger.error(f"Video upload failed: {e}")
                return {
                    "topic": topic,
                    "video": str(video_path),
                    "thumbnail": str(thumb_path),
                    "error": str(e),
                }

        # Fallback return if no upload
        return {"topic": topic, "video": str(video_path), "thumbnail": str(thumb_path)}
