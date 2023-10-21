from repositories.income_repository import default_income_repository


class IncomeService:
    def __init__(self, income_repository=default_income_repository):
        self.income_repository = income_repository

    def insert_income(self, user_id, source, amount):
        self.income_repository.insert_income(user_id, source, amount)

    def get_total_income(self, user_id):
        return self.income_repository.get_total_income(user_id)

    def get_income_past_week(self, user_id):
        return self.income_repository.get_income_past_week(user_id)

    def get_income_past_month(self, user_id):
        return self.income_repository.get_income_past_month(user_id)

    def get_income_past_year(self, user_id):
        return self.income_repository.get_income_past_year(user_id)

    def delete_last_income(self, user_id):
        self.income_repository.delete_last_income(user_id)

    def delete_all_income(self, user_id):
        self.income_repository.delete_all_income(user_id)


default_income_service = IncomeService(default_income_repository)
