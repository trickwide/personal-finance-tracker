from sqlalchemy.sql import text
from db import db
from datetime import datetime, timedelta


def insert_income(user_id, source, amount):
    sql = text(
        "INSERT INTO incomes (user_id, source, amount) VALUES (:user_id, :source, :amount)")

    db.session.execute(
        sql, {"user_id": user_id, "source": source, "amount": amount})

    db.session.commit()


def get_total_income(user_id):
    sql = text(
        "SELECT SUM(amount) FROM incomes WHERE user_id = :user_id")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0]


def get_income_past_week(user_id):
    one_week_ago = datetime.now() - timedelta(days=7)

    sql = text(
        "SELECT SUM(amount) FROM incomes WHERE user_id = :user_id AND date_received > :one_week_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_week_ago": one_week_ago}).fetchone()

    return result[0]


def get_income_past_month(user_id):
    one_month_ago = datetime.now() - timedelta(days=30)

    sql = text(
        "SELECT SUM(amount) FROM incomes WHERE user_id = :user_id AND date_received > :one_month_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_month_ago": one_month_ago}).fetchone()

    return result[0]


def get_income_past_year(user_id):
    one_year_ago = datetime.now() - timedelta(days=365)

    sql = text(
        "SELECT SUM(amount) FROM incomes WHERE user_id = :user_id AND date_received > :one_year_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_year_ago": one_year_ago}).fetchone()

    return result[0]
