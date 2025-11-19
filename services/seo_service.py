from services.llm_service import generate_captions

def suggest_tags(topic: str, n: int = 6) -> list:
    caps = generate_captions(topic, n_lines=4)
    tags = set()
    for c in caps:
        for w in c.replace(',', '').split():
            w = w.strip().lower()
            if len(w) > 3:
                tags.add(w)
            if len(tags) >= n:
                break
        if len(tags) >= n:
            break
    if not tags:
        tags = {'facts','shorts','didyouknow','trivia','funfacts'}
    return list(tags)[:n]
