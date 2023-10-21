from repositories.expense_repository import ExpenseRepository


def insert_expense(user_id, category, amount):
    ExpenseRepository.insert_expense(user_id, category, amount)


def get_total_expense(user_id):
    return ExpenseRepository.get_total_expense(user_id)


def get_expense_past_week(user_id):
    return ExpenseRepository.get_expense_past_week(user_id)


def get_expense_past_month(user_id):
    return ExpenseRepository.get_expense_past_month(user_id)


def get_expense_past_year(user_id):
    return ExpenseRepository.get_expense_past_year(user_id)


def delete_last_expense(user_id):
    ExpenseRepository.delete_last_expense(user_id)


def delete_all_expenses(user_id):
    ExpenseRepository.delete_all_expenses(user_id)
