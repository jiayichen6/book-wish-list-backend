import os
from api.books import books_bp
from api.users import users_bp
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
if cors_origins == "*":
    CORS(app, origins="*")
else:
    origins_list = cors_origins.split(",")
    CORS(app, origins=origins_list)

app.register_blueprint(books_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)
