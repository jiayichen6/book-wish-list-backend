from flask import Flask
from api.books import books_bp
from api.users import users_bp

app = Flask(__name__)
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)
