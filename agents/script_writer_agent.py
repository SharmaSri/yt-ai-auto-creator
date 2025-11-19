"""
ScriptWriterAgent
- Reads prompt template and converts topic into 4-6 short captions suitable for 30s short.
- Uses a small deterministic template to avoid dependence on external LLMs.
"""

class ScriptWriterAgent:
    def __init__(self):
        pass

    def write_script(self, topic: str) -> list[str]:
        caps = []
        # Try to split on colon or comma
        if ':' in topic:
            part = topic.split(':', 1)[1].strip()
        elif ',' in topic:
            part = topic.split(',', 1)[0].strip()
        else:
            part = topic

        # Create simple catchy captions
        caps.append(part if len(part) <= 30 else part[:30].rstrip() + "...")
        caps.append('Did you know? ' + (part if len(part) <= 24 else part[:24].rstrip() + "..."))
        caps.append('Fun fact: ' + (part if len(part) <= 20 else part[:20].rstrip() + "..."))
        caps.append('Share if you were surprised!')

        # Ensure 5 captions for pacing
        if len(caps) < 5:
            caps.append('Follow for more facts!')

        return caps

    # Add this to fix DailyAutopilot call
    def read_script_lines(self, topic_or_path) -> list[str]:
        """
        For compatibility: returns captions list from a topic string.
        """
        # If the argument is a path, you could read file text; here we assume topic string
        return self.write_script(str(topic_or_path))
