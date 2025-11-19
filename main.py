import argparse
import os
from workflows.daily_autopilot import DailyAutopilot
from utils.logger import logger

CLIENT_SECRET = "client_secret.json"  # path to your YouTube API credentials

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Do not upload; just create assets')
    parser.add_argument('--upload', action='store_true', help='Attempt to upload to YouTube (requires client_secret.json)')
    args = parser.parse_args()

    # Auto-detect YouTube credentials
    auto_upload = os.path.exists(CLIENT_SECRET)
    
    if args.upload:
        upload_enabled = True
        if not auto_upload:
            logger.warning("Upload requested but client_secret.json not found. Falling back to dry-run.")
            upload_enabled = False
    elif args.dry_run:
        upload_enabled = False
    else:
        # No flags: automatically upload if credentials exist
        upload_enabled = auto_upload

    if upload_enabled:
        logger.info("YouTube upload enabled.")
    else:
        logger.info("Dry-run mode: only creating assets (no upload).")

    pipeline = DailyAutopilot(upload=upload_enabled)
    res = pipeline.run_once(dry_run=not upload_enabled)
    
    logger.info("Pipeline finished: %s", res)
    print("Result:", res)
