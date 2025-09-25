# Book Wish List API

一個提供註冊、登入、書單管理的 RESTful API，使用 Python + Flask 製作。

## 技術

- Python 3.13
- Flask
- JSON 檔案儲存（模擬資料庫）
- JWT 驗證機制
- dotenv 管理環境變數
- threading.RLock（單進程檔案寫入鎖）

## 功能簡介

- 使用者註冊 / 登入
- JWT 身分驗證
- 取得全書列表（公開）
- 加入 / 移除個人書單
- 書單分類：想讀、已讀、收藏

## 認證方式

需要驗證的 API 請在 Header 加上：
**Authorization: "Bearer <your_jwt_token>"**

## API 路由設計

| Method | Path                                     | 說明             | 驗證 | 請求格式                                   | 回應格式（成功）                                             |
| ------ | ---------------------------------------- | ---------------- | ---- | ------------------------------------------ | ------------------------------------------------------------ |
| POST   | `/users/register`                        | 註冊帳號         | No   | `{"account":"string","password":"string"}` | `{"message":"註冊成功"}`                                     |
| POST   | `/users/login`                           | 登入帳號         | No   | `{"account":"string","password":"string"}` | `{"message":"登入成功","token":"<JWT>"}`                     |
| POST   | `/users/check`                           | 驗證 token       | Yes  | 無                                         | `{"message":"登入驗證成功","account":"<account>"}`           |
| GET    | `/books/`                                | 所有書籍（公開） | No   | 無                                         | `{"allBooksData":{"booksData":{...},"booksDescData":[...]}}` |
| GET    | `/books/my/<list_name>`                  | 使用者某書單     | Yes  | 無                                         | `["<book_key>", "<book_key>", ...]`                          |
| POST   | `/books/my/<list_name>/<string:book_id>` | 加入該書單       | Yes  | 無                                         | `{"message":"新增書本成功","book_keys":["<book_key>", ...]}` |
| DELETE | `/books/my/<list_name>/<string:book_id>` | 自該書單移除     | Yes  | 無                                         | `{"message":"移除書本成功","book_keys":["<book_key>", ...]}` |

> 補充說明：toReadBooks 與 finishedBooks 互斥，後端在 POST 時會自動把該 book_id 從另一個互斥清單移除；favoriteBooks 不互斥。

### 書單分類 (list_name)

- `toReadBooks`: 想讀
- `finishedBooks`: 已讀
- `favoriteBooks`: 收藏

## 設置說明

- 請建立 `data/users.json` ，並加入：[]

- 請建立 `data/user_books.json` ，並加入：{}

- 請參照 `.env.example` 建立 `.env` 檔案，並加入：
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
