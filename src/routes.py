from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import secrets
from db import db
import services.user_service
import services.income_service
from services.expense_service import default_expense_service
import services.saving_service
from services.budget_service import default_budget_service
from services.goal_service import default_goal_service


def check_session():
    return "username" in session


def validate_csrf_token(request_token):
    return request_token == session["csrf_token"]


@app.route("/", methods=["GET", "POST"])
def index():
    if check_session():
        flash(
            "You are already logged in. Please log out, if you wish to log in with a different account.")
        return redirect(url_for('dashboard'))

    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("frontend/index.html")

    if request.method == "POST":
        if not validate_csrf_token(request.form.get("csrf_token")):
            flash("Invalid CSRF token")
            return redirect(url_for('index'))

        username = request.form.get("username")
        password = request.form.get("password")

        valid = services.user_service.validate_user_credentials(
            username, password)

        if not valid:
            flash("Invalid username or password")
            return redirect(url_for('index'))

        session["username"] = username

        return redirect(url_for('dashboard'))

    return render_template("frontend/index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])

        if user_id:
            income_data = {
                "total": services.income_service.get_total_income(user_id),
                "week": services.income_service.get_income_past_week(user_id),
                "month": services.income_service.get_income_past_month(user_id),
                "year": services.income_service.get_income_past_year(user_id)
            }

            expense_data = {
                "total": default_expense_service.get_total_expense(user_id),
                "week": default_expense_service.get_expense_past_week(
                    user_id),
                "month": default_expense_service.get_expense_past_month(
                    user_id),
                "year": default_expense_service.get_expense_past_year(
                    user_id)
            }

            savings_data = {
                "total": services.saving_service.total_savings(user_id),
                "emergency": services.saving_service.get_emergency_savings(user_id),
                "retirement": services.saving_service.get_retirement_savings(user_id),
                "investment": services.saving_service.get_investment_savings(user_id)
            }

            budget_data = {
                "housing": default_budget_service.get_housing_utilities_budget(user_id),
                "food": default_budget_service.get_food_transport_budget(user_id),
                "health": default_budget_service.get_health_personal_budget(user_id),
                "lifestyle": default_budget_service.get_lifestyle_misc_budget(user_id)
            }

            financial_goals = default_goal_service.get_all_goals_for_user(
                user_id)

            return render_template("frontend/dashboard.html", income=income_data, expense=expense_data, savings=savings_data, budget=budget_data, goals=financial_goals)

    return render_template("frontend/dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if check_session():
        flash("You are already logged in. Please log out to create a new account.")
        return redirect(url_for('dashboard'))

    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("frontend/register.html")

    if request.method == "POST":
        if not validate_csrf_token(request.form.get("csrf_token")):
            flash("Invalid CSRF token")
            return redirect(url_for('register'))

        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if password != password_confirm:
            flash("Passwords do not match")
            return redirect(url_for('register'))

        username_valid, username_error = services.user_service.is_username_valid(
            username)
        if not username_valid:
            flash(username_error)
            return redirect(url_for('register'))

        password_valid, password_error = services.user_service.is_password_valid(
            password)
        if not password_valid:
            flash(password_error)
            return redirect(url_for('register'))

        try:
            services.user_service.register_user(username, password)
            flash("Registration successful")
            return redirect(url_for('index'))
        except ValueError as error:
            print(f"Error: {str(error)}")
            flash("An error occurred. Please try again.")
            return redirect(url_for('register'))

    return render_template("frontend/register.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for('index'))


@app.route("/add_income", methods=["POST"])
def add_income():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    source = request.form.get("source")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            services.income_service.insert_income(user_id, source, amount)
            flash("Income added successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to add income")
        return redirect(url_for('index'))


@app.route("/delete_last_income", methods=["POST"])
def delete_last_income():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            services.income_service.delete_last_income(user_id)
            flash("Last income transaction deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete income transactions")
        return redirect(url_for('index'))


@app.route("/delete_all_income", methods=["POST"])
def delete_all_income():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            services.income_service.delete_all_income(user_id)
            flash("All income transactions deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete income transactions")
        return redirect(url_for('index'))


@app.route("/add_expense", methods=["POST"])
def add_expense():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])

        if user_id:
            default_expense_service.insert_expense(user_id, category, amount)
            flash("Expense added successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to add expense")
        return redirect(url_for('index'))


@app.route("/delete_last_expense", methods=["POST"])
def delete_last_expense():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_expense_service.delete_last_expense(user_id)
            flash("Last expense transaction deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete expense transactions")
        return redirect(url_for('index'))


@app.route("/delete_all_expense", methods=["POST"])
def delete_all_expenses():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_expense_service.delete_all_expenses(user_id)
            flash("All expense transactions deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete expense transactions")
        return redirect(url_for('index'))


@app.route("/add_saving", methods=["POST"])
def add_saving():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])

        if user_id:
            services.saving_service.insert_saving(user_id, category, amount)
            flash("Saving added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add saving")
        return redirect(url_for('index'))


@app.route("/delete_last_saving", methods=["POST"])
def delete_last_saving():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            services.saving_service.delete_last_saving(user_id)
            flash("Last saving transaction deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete saving transactions")
        return redirect(url_for('index'))


@app.route("/delete_all_savings", methods=["POST"])
def delete_all_savings():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            services.saving_service.delete_all_savings(user_id)
            flash("All saving transactions deleted successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to delete saving transactions")
        return redirect(url_for('index'))


@app.route("/add_budget", methods=["POST"])
def add_budget():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])

        if user_id:
            default_budget_service.insert_budget(user_id, category, amount)
            flash("Budget added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add budget")
        return redirect(url_for('index'))


@app.route("/delete_last_budget", methods=["POST"])
def delete_last_budget():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_budget_service.delete_last_budget(user_id)
            flash("Last budget transaction deleted successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to delete budget transactions")
        return redirect(url_for('index'))


@app.route("/delete_all_budgets", methods=["POST"])
def delete_all_budgets():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_budget_service.delete_all_budgets(user_id)
            flash("All budget transactions deleted successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to delete budget transactions")
        return redirect(url_for('index'))


@app.route("/add_goal", methods=["POST"])
def add_goal():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    goal_name = request.form.get("name")
    category = request.form.get("category")
    goal_amount = float(request.form.get("amount"))
    target_date = request.form.get("date")

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])

        if user_id:

            if not default_goal_service.is_goal_name_unique(user_id, goal_name):
                flash("Goal name already exists. Please choose an unique name.")
                return redirect(url_for('dashboard'))

            default_goal_service.insert_goal(
                user_id, goal_name, category, goal_amount, target_date)
            flash("Financial goal added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add financial goal")
        return redirect(url_for('index'))


@app.route("/delete_last_goal", methods=["POST"])
def delete_last_goal():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_goal_service.delete_last_goal(user_id)
            flash("Last goal deleted successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to delete goals")
        return redirect(url_for('index'))


@app.route("/delete_all_goals", methods=["POST"])
def delete_all_goals():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            default_goal_service.delete_all_goals(user_id)
            flash("All goals deleted successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to delete goals")
        return redirect(url_for('index'))


@app.route("/delete_goal_by_name", methods=["POST"])
def delete_goal_by_name():
    if not validate_csrf_token(request.form.get("csrf_token")):
        flash("Invalid CSRF token")
        return redirect(url_for('dashboard'))

    if check_session():
        user_id = services.user_service.get_user_id_by_username(
            session["username"])
        if user_id:
            goal_name = request.form.get("name")
            if default_goal_service.delete_goal_by_name(user_id, goal_name):
                flash("Goal deleted successfully")
            else:
                flash("Goal not found!")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to delete goals")
        return redirect(url_for('index'))
