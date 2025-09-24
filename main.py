import re
from api.books import books_bp
from api.users import users_bp
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

CORS(app, origins=[re.compile(r"http://localhost:\d+")])

app.register_blueprint(books_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)
