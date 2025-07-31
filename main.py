from flask import Flask, jsonify, request
import json
import uuid

app = Flask(__name__)


# test
@app.route("/")
def hello():
    return "Hello, Flask! 第一隻 API 成功了"


@app.route("/books", methods=["GET"])
def get_books():
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
            return jsonify(books), 200

    except FileNotFoundError:
        return jsonify({"error": "讀取書本資料失敗"}), 404


@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.get_json()

    if not new_book or "title" not in new_book or "author" not in new_book:
        return jsonify({"error": "書本格式錯誤"}), 400

    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
            new_book["id"] = str(uuid.uuid4())
            books.append(new_book)

        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False)

        return jsonify({"message": "新增書本成功"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "新增書本失敗"}), 400


@app.route("/books/<string:book_id>", methods=["PATCH"])
def update_book(book_id):
    update_book = request.get_json()
    print(update_book)

    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
            target_book = next((b for b in books if b["id"] == book_id), None)

            if target_book is None:
                return jsonify({"error": "查無此本書"}), 404

            target_book.update(update_book)
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False)

            return jsonify({"message": "成功修改書本"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "修改書本失敗"}), 400


@app.route("/books/<string:book_id>", methods=["DELETE"])
def delete_book(book_id):

    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
            target_book = next((b for b in books if b["id"] == book_id), None)

            if target_book is None:
                return jsonify({"error": "查無此本書"}), 404

            books.remove(target_book)

            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False)
            return jsonify({"message": "刪除書本成功"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "刪除書本失敗"}), 400


if __name__ == "__main__":
    app.run(debug=True)
