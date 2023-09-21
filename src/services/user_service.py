from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from test_db import db


def register_user(username, password):
    # Check if username already exists
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result:
        raise ValueError("Username already exists")

    # Hash the password
    hashed_password = generate_password_hash(password)

    sql = text(
        "INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(
        sql, {"username": username, "password": hashed_password})
    db.session.commit()
