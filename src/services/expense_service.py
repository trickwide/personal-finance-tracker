from repositories.expense_repository import default_expense_repository


class ExpenseService:
    def __init__(self, expense_repository=default_expense_repository):
        self.expense_repository = expense_repository

    def insert_expense(self, user_id, category, amount):
        self.expense_repository.insert_expense(
            user_id, category, amount)

    def get_total_expense(self, user_id):
        return self.expense_repository.get_total_expense(user_id)

    def get_expense_past_week(self, user_id):
        return self.expense_repository.get_expense_past_week(user_id)

    def get_expense_past_month(self, user_id):
        return self.expense_repository.get_expense_past_month(user_id)

    def get_expense_past_year(self, user_id):
        return self.expense_repository.get_expense_past_year(user_id)

    def delete_last_expense(self, user_id):
        self.expense_repository.delete_last_expense(user_id)

    def delete_all_expenses(self, user_id):
        self.expense_repository.delete_all_expenses(user_id)


default_expense_service = ExpenseService(default_expense_repository)
