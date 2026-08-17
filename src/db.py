import json
import os

from src.config import DB_PATH


def create_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)


def read_db() -> dict:
    if not os.path.exists(DB_PATH):
        create_db()

    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db: dict) -> None:
    if not os.path.exists(DB_PATH):
        create_db()

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f)
