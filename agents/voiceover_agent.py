"""
VoiceoverAgent — Not used in Quotes-on-screen format. Included for compatibility.
It returns None to indicate no audio narration; video editor will optionally add background music.
"""
class VoiceoverAgent:
    def __init__(self):
        pass

    def generate_voice(self, script_lines:list):
        # No narration for quotes-only short.
        return None