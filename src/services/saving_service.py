from repositories.saving_repository import default_saving_repository


class SavingService:
    def __init__(self, saving_repository=default_saving_repository):
        self.saving_repository = saving_repository

    def insert_saving(self, user_id, category, amount):
        self.saving_repository.insert_saving(user_id, category, amount)

    def total_savings(self, user_id):
        return self.saving_repository.total_savings(user_id)

    def get_emergency_savings(self, user_id):
        return self.saving_repository.get_emergency_savings(user_id)

    def get_retirement_savings(self, user_id):
        return self.saving_repository.get_retirement_savings(user_id)

    def get_investment_savings(self, user_id):
        return self.saving_repository.get_investment_savings(user_id)

    def delete_last_saving(self, user_id):
        self.saving_repository.delete_last_saving(user_id)

    def delete_all_savings(self, user_id):
        self.saving_repository.delete_all_savings(user_id)


default_saving_service = SavingService(default_saving_repository)
