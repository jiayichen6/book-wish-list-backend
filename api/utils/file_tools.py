from pathlib import Path
import json

base_dir = Path(__file__).resolve().parent.parent.parent
# 回到根目錄

users_path = base_dir / "data" / "users.json"
all_books_path = base_dir / "data" / "all_books.json"
user_books_path = base_dir / "data" / "user_books.json"


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
