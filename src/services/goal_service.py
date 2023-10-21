from repositories.goal_repository import default_goal_repository


class GoalService:
    def __init__(self, goal_repository=default_goal_repository):
        self.goal_repository = goal_repository

    def get_current_amount_for_goal(self, user_id, category):
        return self.goal_repository.get_current_amount_for_goal(user_id, category)

    def get_all_goals_for_user(self, user_id):
        return self.goal_repository.get_all_goals_for_user(user_id)

    def insert_goal(self, user_id, goal_name, category, goal_amount, target_date):
        self.goal_repository.insert_goal(
            user_id, goal_name, category, goal_amount, target_date)

    def is_goal_name_unique(self, user_id, goal_name):
        return self.goal_repository.is_goal_name_unique(user_id, goal_name)

    def delete_last_goal(self, user_id):
        self.goal_repository.delete_last_goal(user_id)

    def delete_all_goals(self, user_id):
        self.goal_repository.delete_all_goals(user_id)

    def delete_goal_by_name(self, user_id, goal_name):
        return self.goal_repository.delete_goal_by_name(user_id, goal_name)


default_goal_service = GoalService(default_goal_repository)
