# Book Wish List API

一個提供註冊、登入、書單管理的 RESTful API，使用 Python + Flask 製作。

## 技術

- Python 3.13
- Flask
- JSON 檔案儲存（模擬資料庫）
- JWT 驗證機制
- dotenv 管理環境變數

## 功能簡介

- 使用者註冊 / 登入
- JWT 身分驗證
- 取得全書列表（公開）
- 加入 / 移除個人書單
- 書單分類：想讀、已讀、收藏

## API 路由設計

| Method | Path                                     | 說明       | 驗證 |
| ------ | ---------------------------------------- | ---------- | ---- |
| POST   | `/users/register`                        | 註冊帳號   | No   |
| POST   | `/users/login`                           | 登入帳號   | No   |
| POST   | `/users/check`                           | 驗證 token | Yes  |
| GET    | `/books`                                 | 所有書籍   | No   |
| GET    | `/books/my/<list_name>`                  | 我的某書單 | Yes  |
| POST   | `/books/my/<list_name>/<string:book_id>` | 加入書單   | Yes  |
| DELETE | `/books/my/<list_name>/<string:book_id>` | 移出書單   | Yes  |

## 設置說明

- 請建立 `data/users.json` ，並加入：[]

- 請建立 `.env` 檔案，並加入：
  SECRET_KEY=your_secret_key_here
  （你可以自行定義一組安全的密鑰。）

## 本地啟動方式

```bash
make server
# 或
uv run python -m flask --app main run
```

by Jia Yi Chen
s709161616@gmail.com
