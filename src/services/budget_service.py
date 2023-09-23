from sqlalchemy.sql import text
from db import db


def insert_budget(user_id, category, amount):
    sql = text(
        "INSERT INTO budgets (user_id, category, amount) VALUES (:user_id, :category, :amount)")

    db.session.execute(
        sql, {"user_id": user_id, "category": category, "amount": amount})

    db.session.commit()


def get_housing_utilities_budget(user_id):
    sql = text(
        "SELECT SUM(amount) FROM budgets WHERE user_id = :user_id AND category = 'housing_utilities'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_food_transport_budget(user_id):
    sql = text(
        "SELECT SUM(amount) FROM budgets WHERE user_id = :user_id AND category = 'food_transport'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_health_personal_budget(user_id):
    sql = text(
        "SELECT SUM(amount) FROM budgets WHERE user_id = :user_id AND category = 'health_personal'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_lifestyle_misc_budget(user_id):
    sql = text(
        "SELECT SUM(amount) FROM budgets WHERE user_id = :user_id AND category = 'lifestyle_misc'")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0
