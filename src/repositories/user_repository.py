from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class UserRepository:
    def validate_user_credentials(self, username, password):
        sql = text("SELECT password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username}).fetchone()
        if not result:
            return False

        hashed_password = result[0]
        return check_password_hash(hashed_password, password)

    def register_user(self, username, password):
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

    def get_user_id_by_username(self, username):
        sql = text("SELECT user_id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username}).fetchone()
        return result.user_id if result else None

    def delete_user(self, user_id):
        sql = text("DELETE FROM users WHERE user_id=:user_id")
        db.session.execute(sql, {"user_id": user_id})
        db.session.commit()


default_user_repository = UserRepository()
