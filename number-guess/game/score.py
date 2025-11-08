# game/score.py
import json
from pathlib import Path
from typing import List, Dict

# Store highscores relative to this file's parent package, not CWD.
BASE_DIR = Path(__file__).resolve().parent.parent  # points to project root that contains 'game'
HIGHSCORES_PATH = BASE_DIR / "data" / "highscores.json"

def ensure_data_file():
    HIGHSCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not HIGHSCORES_PATH.exists():
        # create an empty list as JSON
        HIGHSCORES_PATH.write_text("[]", encoding="utf-8")

def load_highscores() -> List[Dict]:
    ensure_data_file()
    try:
        with HIGHSCORES_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            # if file contains something else, reset to empty list
            return []
    except Exception:
        # if file corrupted or unreadable, reset it
        HIGHSCORES_PATH.write_text("[]", encoding="utf-8")
        return []

def save_highscore(name: str, score: int, attempts: int, difficulty: str):
    ensure_data_file()
    scores = load_highscores()
    scores.append({
        "name": name,
        "score": score,
        "attempts": attempts,
        "difficulty": difficulty
    })
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    with HIGHSCORES_PATH.open("w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    # debug/info: print where we saved the file and the last saved entry
    print(f"[DEBUG] Highscore saved to: {HIGHSCORES_PATH}")
    print(f"[DEBUG] Last entry: {scores[0] if scores else 'none'}")

def pretty_highscores() -> str:
    scores = load_highscores()
    if not scores:
        return "No high scores yet."
    lines = ["=== High Scores ==="]
    for i, s in enumerate(scores, 1):
        lines.append(f"{i}. {s['name']} — {s['score']} pts — {s['attempts']} attempts — {s['difficulty']}")
    return "\n".join(lines)
