from sqlalchemy.sql import text
from db import db


class SavingRepository:
    def insert_saving(self, user_id, category, amount):
        sql = text(
            "INSERT INTO savings (user_id, category, amount) VALUES (:user_id, :category, :amount)")

        db.session.execute(
            sql, {"user_id": user_id, "category": category, "amount": amount})

        db.session.commit()

    def total_savings(self, user_id):
        sql = text(
            "SELECT SUM(amount) FROM savings WHERE user_id = :user_id")

        result = db.session.execute(
            sql, {"user_id": user_id}).fetchone()

        return result[0] or 0.0

    def get_emergency_savings(self, user_id):
        sql = text(
            "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'emergency'")

        result = db.session.execute(
            sql, {"user_id": user_id}).fetchone()

        return result[0] or 0.0

    def get_retirement_savings(self, user_id):
        sql = text(
            "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'retirement'")

        result = db.session.execute(
            sql, {"user_id": user_id}).fetchone()

        return result[0] or 0.0

    def get_investment_savings(self, user_id):
        sql = text(
            "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = 'investment'")

        result = db.session.execute(
            sql, {"user_id": user_id}).fetchone()

        return result[0] or 0.0

    def delete_last_saving(self, user_id):
        sql = text("""
                DELETE FROM savings
                    WHERE saving_id = (
                        SELECT saving_id
                        FROM savings
                        WHERE user_id = :user_id
                        ORDER BY date_saved DESC
                        LIMIT 1)
                    """
                   )

        db.session.execute(sql, {"user_id": user_id})

        db.session.commit()

    def delete_all_savings(self, user_id):
        sql = text(
            "DELETE FROM savings WHERE user_id = :user_id")

        db.session.execute(sql, {"user_id": user_id})

        db.session.commit()


default_saving_repository = SavingRepository()
