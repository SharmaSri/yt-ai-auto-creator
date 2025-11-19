"""
UploadAgent — optional YouTube upload using google-api-python-client.
If OAuth credentials aren't present, upload will be skipped.
"""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils.logger import logger  # optional, for logging

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

class UploadAgent:
    def __init__(self, client_secrets_path: str = None, credentials_path: str = "./youtube_credentials.pkl"):
        """
        :param client_secrets_path: Path to your client_secret.json
        :param credentials_path: Path to save OAuth credentials
        """
        self.client_secrets = client_secrets_path
        self.credentials_path = credentials_path
        self.youtube = self.authenticate()

    def authenticate(self):
        """Authenticate and return YouTube API client."""
        creds = None
        # Load existing credentials
        if os.path.exists(self.credentials_path):
            with open(self.credentials_path, "rb") as f:
                creds = pickle.load(f)

        # If no valid credentials, run OAuth flow
        if not creds:
            if not self.client_secrets or not os.path.exists(self.client_secrets):
                logger.warning("YouTube client secrets not found. Upload will be skipped.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save credentials for future use
            with open(self.credentials_path, "wb") as f:
                pickle.dump(creds, f)

        return build("youtube", "v3", credentials=creds)

    def upload_video(self, video_path: str, thumbnail_path: str = None, title: str = "Untitled", description: str = "", tags: list = None, categoryId: str = "22", privacyStatus: str = "public"):
        """
        Upload a video to YouTube.
        :param video_path: Path to the video file
        :param thumbnail_path: Path to the thumbnail
        :param title: Video title
        :param description: Video description
        :param tags: List of tags
        :param categoryId: YouTube category (default 22 = People & Blogs)
        :param privacyStatus: public, unlisted, private
        :return: video ID if uploaded, else None
        """
        if self.youtube is None:
            logger.warning("YouTube client not initialized. Skipping upload.")
            return None

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags or [],
                    "categoryId": categoryId
                },
                "status": {
                    "privacyStatus": privacyStatus
                }
            },
            media_body=media
        )

        response = None
        try:
            response = request.execute()
            video_id = response.get("id")
            logger.info(f"Video uploaded: https://www.youtube.com/watch?v={video_id}")

            # Set thumbnail if provided
            if thumbnail_path and os.path.exists(thumbnail_path):
                self.youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
                logger.info(f"Thumbnail uploaded: {thumbnail_path}")

            return video_id

        except Exception as e:
            logger.error(f"Failed to upload video: {e}")
            return None
