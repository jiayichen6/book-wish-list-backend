from flask import request, jsonify, Blueprint
from .utils.file_tools import (
    read_json,
    write_json,
    users_path,
)
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from functools import wraps
from dotenv import load_dotenv
from threading import RLock
import os
import re
import datetime
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

user_lock = RLock()


users_bp = Blueprint("users", __name__, url_prefix="/users")


def token_require(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        user_header = request.headers.get("Authorization")

        if not user_header or not user_header.startswith("Bearer "):
            return jsonify({"error": "請帶上token"}), 401

        token = user_header.replace("Bearer ", "").strip()

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return func(*args, **kargs, account=decoded["account"])

        except ExpiredSignatureError:
            return jsonify({"error": "token 過期"}), 401
        except InvalidTokenError:
            return jsonify({"error": "token 無效"}), 401

    return wrapper


@users_bp.route("/register", methods=["POST"])
def register():
    new_user = request.get_json()

    if not new_user or "account" not in new_user or "password" not in new_user:
        return jsonify({"error": "缺少註冊資料"}), 400

    email = new_user["account"]
    email_pattern = r"^[A-Za-z0-9]+[\w\.-]*@[A-Za-z0-9-]+\.[A-Za-z]{2,}$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "email 格式錯誤"}), 400

    password = new_user["password"]
    password_pattern = r"^.{6,20}$"
    if not re.match(password_pattern, password):
        return jsonify({"error": "password 長度要 6～20 字元"}), 400

    try:
        with user_lock:
            user_data = read_json(users_path)

            user_exist = next(
                (user for user in user_data if user["account"] == new_user["account"]),
                None,
            )

            if user_exist:
                return jsonify({"error": "帳號已存在"}), 400

            hashed_password = generate_password_hash(new_user["password"])
            new_user["password"] = hashed_password
            user_data.append(new_user)
            write_json(users_path, user_data)

        return jsonify({"message": "註冊成功"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "註冊失敗"}), 400


@users_bp.route("/login", methods=["POST"])
def log_in():
    user_input = request.get_json()

    if not user_input or "account" not in user_input or "password" not in user_input:
        return jsonify({"error": "缺少登入資料"}), 400

    try:
        user_data = read_json(users_path)

        found_user = next(
            (u for u in user_data if u["account"] == user_input["account"]), None
        )

        if not found_user:
            return jsonify({"error": "帳號不存在"}), 404

        is_password_correct = check_password_hash(
            found_user["password"], user_input["password"]
        )
        if not is_password_correct:
            return jsonify({"error": "密碼錯誤"}), 400

        payload = {
            "account": found_user["account"],
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=2),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "登入成功", "token": token}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "登入失敗"}), 400


@users_bp.route("/check", methods=["POST"])
@token_require
def get_me(account):
    return jsonify({"message": "登入驗證成功", "account": account}), 200
