from sqlalchemy.sql import text
from test_db import db


def insert_income(user_id, source, amount):
    sql = text(
        "INSERT INTO incomes (user_id, source, amount) VALUES (:user_id, :source, :amount)")

    db.session.execute(
        sql, {"user_id": user_id, "source": source, "amount": amount})

    db.session.commit()
