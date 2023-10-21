from sqlalchemy.sql import text
from db import db
from datetime import datetime, timedelta


def insert_expense(user_id, category, amount):
    sql = text(
        "INSERT INTO expenses (user_id, category, amount) VALUES (:user_id, :category, :amount)")

    db.session.execute(
        sql, {"user_id": user_id, "category": category, "amount": amount})

    db.session.commit()


def get_total_expense(user_id):
    sql = text(
        "SELECT SUM(amount) FROM expenses WHERE user_id = :user_id")

    result = db.session.execute(
        sql, {"user_id": user_id}).fetchone()

    return result[0] or 0.0


def get_expense_past_week(user_id):
    one_week_ago = datetime.now() - timedelta(days=7)

    sql = text(
        "SELECT SUM(amount) FROM expenses WHERE user_id = :user_id AND date_incurred > :one_week_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_week_ago": one_week_ago}).fetchone()

    return result[0] or 0.0


def get_expense_past_month(user_id):
    one_month_ago = datetime.now() - timedelta(days=30)

    sql = text(
        "SELECT SUM(amount) FROM expenses WHERE user_id = :user_id AND date_incurred > :one_month_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_month_ago": one_month_ago}).fetchone()

    return result[0] or 0.0


def get_expense_past_year(user_id):
    one_year_ago = datetime.now() - timedelta(days=365)

    sql = text(
        "SELECT SUM(amount) FROM expenses WHERE user_id = :user_id AND date_incurred > :one_year_ago"
    )

    result = db.session.execute(
        sql, {"user_id": user_id, "one_year_ago": one_year_ago}).fetchone()

    return result[0] or 0.0


def delete_last_expense(user_id):
    sql = text("""
               DELETE FROM expenses
               WHERE expense_id = (
                   SELECT expense_id
                   FROM expenses
                   WHERE user_id = :user_id
                   ORDER BY date_incurred DESC
                   LIMIT 1
               )
               """
               )

    db.session.execute(
        sql, {"user_id": user_id})

    db.session.commit()


def delete_all_expenses(user_id):
    sql = text(
        "DELETE FROM expenses WHERE user_id = :user_id"
    )

    db.session.execute(
        sql, {"user_id": user_id})

    db.session.commit()
