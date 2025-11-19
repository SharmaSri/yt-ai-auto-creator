from workflows.daily_autopilot import DailyAutopilot

def create_video_once(dry_run=True):
    auto = DailyAutopilot(upload=False)
    return auto.run_once(dry_run=dry_run)
