"""Flask application factory and database initialization."""

import sqlite3
from pathlib import Path
from flask import Flask


def init_db(app: Flask) -> None:
    """Create the SQLite database and seed it if it does not exist."""

    db_path = app.config['DATABASE']
    if not Path(db_path).exists():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "password"),
        )
        conn.commit()
        conn.close()


def create_app() -> Flask:
    """Instantiate and configure the Flask application."""

    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['DATABASE'] = str(Path(app.root_path) / 'database.db')

    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)
    return app
