from agents.upload_agent import UploadAgent

def upload(video_path, thumbnail_path, title):
    upl = UploadAgent()
    return upl.upload_video(video_path, thumbnail_path, title)
