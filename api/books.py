from flask import Blueprint, jsonify
from .users import token_require
from .utils.file_tools import read_json, write_json, all_books_path, user_books_path

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/", methods=["GET"])
def get_all_books():
    try:
        all_books = read_json(all_books_path)
        return jsonify(all_books), 200

    except FileNotFoundError:
        return jsonify({"error": "讀取書本資料失敗"}), 404


@books_bp.route("/user_books/<list_name>", methods=["GET"])
@token_require
def get_user_book_keys(account, list_name):
    try:
        user_books = read_json(user_books_path)

        user_lists = user_books.get(account, {})
        book_keys = user_lists.get(list_name, [])
        return jsonify(book_keys), 200

    except FileNotFoundError:
        return jsonify({"error": "讀取使用者書單失敗"}), 404


@books_bp.route("/user_books/<list_name>/<string:book_id>", methods=["POST"])
@token_require
def add_book(account, list_name, book_id):

    if not list_name or not book_id:
        return jsonify({"error": "書本格式錯誤"}), 400

    exclusive_list = {
        "toReadBooks": ["finishedBooks"],
        "finishedBooks": ["toReadBooks"],
    }

    try:
        all_user_books = read_json(user_books_path)

        all_user_books.setdefault(account, {})
        user_lists = all_user_books[account]
        user_lists.setdefault(list_name, [])
        book_keys = user_lists[list_name]

        if book_id not in book_keys:
            book_keys.append(book_id)

        for other_list in exclusive_list.get(list_name, []):
            if book_id in user_lists.get(other_list, []):
                user_lists[other_list].remove(book_id)

        write_json(user_books_path, all_user_books)

        return jsonify({"message": "新增書本成功", "book_keys": book_keys}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "新增書本失敗"}), 400


@books_bp.route("/user_books/<list_name>/<string:book_id>", methods=["DELETE"])
@token_require
def delete_book(account, list_name, book_id):
    try:
        user_books = read_json(user_books_path)

        if account not in user_books:
            return jsonify({"error": "使用者不存在"}), 404

        user_lists = user_books[account]

        if list_name not in user_lists:
            return jsonify({"error": "清單不存在"}), 404

        book_keys = user_lists[list_name]

        if book_id not in book_keys:
            return jsonify({"error": "書本不在清單中"}), 404

        book_keys.remove(book_id)

        write_json(user_books_path, user_books)
        return jsonify({"message": "刪除書本成功", "book_key": book_keys}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "刪除書本失敗"}), 400
