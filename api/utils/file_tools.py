import json
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent
# 回到根目錄

users_filename = os.getenv("USERS_FILE", "users.json")
user_books_filename = os.getenv("USER_BOOKS_FILE", "user_books.json")

all_books_path = base_dir / "data" / "all_books.json"
users_path = base_dir / "data" / users_filename
user_books_path = base_dir / "data" / user_books_filename


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
