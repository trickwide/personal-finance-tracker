from sqlalchemy.sql import text
from db import db
from datetime import datetime, timedelta


def insert_saving(user_id, category, amount):
    sql = text(
        "INSERT INTO savings (user_id, category, amount) VALUES (:user_id, :category, :amount)")

    db.session.execute(
        sql, {"user_id": user_id, "category": category, "amount": amount})

    db.session.commit()


def total_savings(user_id):
    sql = text(
        "SELECT SUM(amount) FROM savings WHERE user_id = :user_id")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_emergency_savings(user_id):
    sql = text(
        "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'emergency'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_retirement_savings(user_id):
    sql = text(
        "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'retirement'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_investment_savings(user_id):
    sql = text(
        "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'investment'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0
