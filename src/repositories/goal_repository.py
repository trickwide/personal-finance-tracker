from sqlalchemy.sql import text
from db import db
from decimal import Decimal


class GoalRepository:
    def get_current_amount_for_goal(self, user_id, category):
        sql = text(
            "SELECT SUM(amount) FROM savings WHERE user_id = :user_id AND category = :category")

        result = db.session.execute(
            sql, {"user_id": user_id, "category": category}).fetchone()

        return result[0] or 0.0

    def get_all_goals_for_user(self, user_id):
        sql = text("""
                SELECT goal_name, category, goal_amount, target_date
                FROM financial_goals
                WHERE user_id = :user_id
                """
                   )

        result = db.session.execute(sql, {"user_id": user_id}).fetchall()

        columns = ['goal_name', 'category', 'goal_amount', 'target_date']

        goals = [dict(zip(columns, row)) for row in result]

        for goal in goals:
            goal['current_amount'] = Decimal(self.get_current_amount_for_goal(
                user_id, goal['category']))
            goal['goal_amount'] = Decimal(goal['goal_amount'])

        return goals

    def insert_goal(self, user_id, goal_name, category, goal_amount, target_date):
        sql = text("""
                INSERT INTO financial_goals
                    (user_id, goal_name, category, goal_amount, target_date)
                    VALUES
                    (:user_id, :goal_name, :category, :goal_amount, :target_date)
                    """
                   )

        db.session.execute(sql, {"user_id": user_id, "goal_name": goal_name, "category": category,
                                 "goal_amount": goal_amount, "target_date": target_date})

        db.session.commit()

    def is_goal_name_unique(self, user_id, goal_name):
        sql = text(
            "SELECT 1 FROM financial_goals WHERE user_id = :user_id AND goal_name = :goal_name LIMIT 1")

        result = db.session.execute(
            sql, {"user_id": user_id, "goal_name": goal_name}).fetchone()

        return result is None

    def delete_last_goal(self, user_id):
        sql = text("""
                DELETE FROM financial_goals
                WHERE goal_id = (
                        SELECT goal_id
                        FROM financial_goals
                        WHERE user_id = :user_id
                        ORDER BY date_created DESC
                        LIMIT 1)
                """
                   )

        db.session.execute(sql, {"user_id": user_id})

        db.session.commit()

    def delete_all_goals(self, user_id):
        sql = text(
            "DELETE FROM financial_goals WHERE user_id = :user_id")

        db.session.execute(sql, {"user_id": user_id})

        db.session.commit()

    def delete_goal_by_name(self, user_id, goal_name):
        sql = text(
            "DELETE FROM financial_goals WHERE user_id = :user_id AND goal_name = :goal_name")

        result = db.session.execute(
            sql, {"user_id": user_id, "goal_name": goal_name})

        db.session.commit()

        return result.rowcount > 0


default_goal_repository = GoalRepository()
