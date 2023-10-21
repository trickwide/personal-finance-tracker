from repositories.budget_repository import default_budget_repository


class BudgetService:
    def __init__(self, budget_repository=default_budget_repository):
        self.budget_repository = budget_repository

    def insert_budget(self, user_id, category, amount):
        self.budget_repository.insert_budget(user_id, category, amount)

    def get_housing_utilities_budget(self, user_id):
        return self.budget_repository.get_housing_utilities_budget(user_id)

    def get_food_transport_budget(self, user_id):
        return self.budget_repository.get_food_transport_budget(user_id)

    def get_health_personal_budget(self, user_id):
        return self.budget_repository.get_health_personal_budget(user_id)

    def get_lifestyle_misc_budget(self, user_id):
        return self.budget_repository.get_lifestyle_misc_budget(user_id)

    def delete_last_budget(self, user_id):
        self.budget_repository.delete_last_budget(user_id)

    def delete_all_budgets(self, user_id):
        self.budget_repository.delete_all_budgets(user_id)


default_budget_service = BudgetService(default_budget_repository)
