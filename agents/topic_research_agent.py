"""
TopicResearchAgent
- For free mode: reads from local seed file `data/quotes_seed.txt`.
- Optionally: can scrape a simple web source for trending facts.
Returns a short topic/fact string.
"""
import random
from pathlib import Path

SEED_FILE = Path('data/quotes_seed.txt')

class TopicResearchAgent:
    def __init__(self):
        pass

    def suggest_topic(self) -> str:
        if SEED_FILE.exists():
            lines = [l.strip() for l in SEED_FILE.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
            if lines:
                return random.choice(lines)
        # Fallback static
        fallback = 'Interesting fact about space: black holes are not actually holes.'
        return fallback