from flask import Blueprint, request, jsonify
from pathlib import Path
import json
import uuid

books_bp = Blueprint("books", __name__, url_prefix="/books")
base_dir = Path(__file__).resolve().parent.parent
# 回到根目錄
data_path = base_dir / "data" / "books.json"


@books_bp.route("/", methods=["GET"])
def get_books():
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            books = json.load(f)
            return jsonify(books), 200

    except FileNotFoundError:
        return jsonify({"error": "讀取書本資料失敗"}), 404


@books_bp.route("/", methods=["POST"])
def add_book():
    new_book = request.get_json()

    if not new_book or "title" not in new_book or "author" not in new_book:
        return jsonify({"error": "書本格式錯誤"}), 400

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            books = json.load(f)
            new_book["id"] = str(uuid.uuid4())
            books.append(new_book)

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False)

        return jsonify({"message": "新增書本成功"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "新增書本失敗"}), 400


@books_bp.route("/<string:book_id>", methods=["PATCH"])
def update_book(book_id):
    update_book = request.get_json()
    print(update_book)

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            books = json.load(f)
            target_book = next((b for b in books if b["id"] == book_id), None)

            if target_book is None:
                return jsonify({"error": "查無此本書"}), 404

            target_book.update(update_book)
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False)

            return jsonify({"message": "成功修改書本"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "修改書本失敗"}), 400


@books_bp.route("/<string:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            books = json.load(f)
            target_book = next((b for b in books if b["id"] == book_id), None)

            if target_book is None:
                return jsonify({"error": "查無此本書"}), 404

            books.remove(target_book)

            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False)
            return jsonify({"message": "刪除書本成功"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "刪除書本失敗"}), 400
