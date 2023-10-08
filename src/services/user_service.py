from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import re


def is_username_valid(username):
    if len(username) < 5:
        return False, "Username is too short. Minimum length is 5 characters"

    if not re.match("^[a-zA-Z0-9_]*$", username):
        return False, "Username can only contain letters, numbers and underscores"

    if username.isdigit():
        return False, "Username cannot be a number"

    return True, None


def is_password_valid(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."

    if not bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False, "Password must contain at least one special character (e.g., !@#$%^&*)."

    return True, None


def validate_user_credentials(username, password):
    sql = text("SELECT password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    if not result:
        return False

    hashed_password = result[0]
    return check_password_hash(hashed_password, password)


def register_user(username, password):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result:
        raise ValueError("Username already exists")

    hashed_password = generate_password_hash(password)

    sql = text(
        "INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(
        sql, {"username": username, "password": hashed_password})
    db.session.commit()


def get_user_id_by_username(username):
    sql = text("SELECT user_id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    return result.user_id if result else None
