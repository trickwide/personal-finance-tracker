from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from db import db
from services.user_service import register_user, is_username_valid, is_password_valid, validate_user_credentials, get_user_id_by_username
from services.income_service import insert_income, get_total_income, get_income_past_week, get_income_past_month, get_income_past_year
import services.expense_service
import services.saving_service
import services.budget_service
import services.goal_service


def check_session():
    return "username" in session


@app.route("/", methods=["GET", "POST"])
def index():
    if check_session():
        flash(
            "You are already logged in. Please log out, if you wish to log in with a different account.")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        valid = validate_user_credentials(username, password)

        if not valid:
            flash("Invalid username or password")
            return redirect(url_for('index'))

        session["username"] = username
        return redirect(url_for('dashboard'))

    return render_template("frontend/index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if check_session():
        user_id = get_user_id_by_username(session["username"])

        if user_id:
            income_data = {
                "total": get_total_income(user_id),
                "week": get_income_past_week(user_id),
                "month": get_income_past_month(user_id),
                "year": get_income_past_year(user_id)
            }

            expense_data = {
                "total": services.expense_service.get_total_expense(user_id),
                "week": services.expense_service.get_expense_past_week(
                    user_id),
                "month": services.expense_service.get_expense_past_month(
                    user_id),
                "year": services.expense_service.get_expense_past_year(
                    user_id)
            }

            savings_data = {
                "total": services.saving_service.total_savings(user_id),
                "emergency": services.saving_service.get_emergency_savings(user_id),
                "retirement": services.saving_service.get_retirement_savings(user_id),
                "investment": services.saving_service.get_investment_savings(user_id)
            }

            budget_data = {
                "housing": services.budget_service.get_housing_utilities_budget(user_id),
                "food": services.budget_service.get_food_transport_budget(user_id),
                "health": services.budget_service.get_health_personal_budget(user_id),
                "lifestyle": services.budget_service.get_lifestyle_misc_budget(user_id)
            }

            financial_goals = services.goal_service.get_all_goals_for_user(
                user_id)

            return render_template("frontend/dashboard.html", income=income_data, expense=expense_data, savings=savings_data, budget=budget_data, goals=financial_goals)

    return render_template("frontend/dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if check_session():
        flash("You are already logged in. Please log out to create a new account.")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if password != password_confirm:
            flash("Passwords do not match")
            return redirect(url_for('register'))

        username_valid, username_error = is_username_valid(username)
        if not username_valid:
            flash(username_error)
            return redirect(url_for('register'))

        password_valid, password_error = is_password_valid(password)
        if not password_valid:
            flash(password_error)
            return redirect(url_for('register'))

        try:
            register_user(username, password)
            flash("Registration successful")
            return redirect(url_for('index'))
        except ValueError as error:
            flash(str(error))
            return redirect(url_for('register'))

    return render_template("frontend/register.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for('index'))


@app.route("/add_income", methods=["POST"])
def add_income():
    source = request.form.get("source")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = get_user_id_by_username(session["username"])
        if user_id:
            insert_income(user_id, source, amount)
            flash("Income added successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to add income")
        return redirect(url_for('index'))


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = get_user_id_by_username(session["username"])

        if user_id:
            services.expense_service.insert_expense(user_id, category, amount)
            flash("Expense added successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to add expense")
        return redirect(url_for('index'))


@app.route("/add_saving", methods=["POST"])
def add_saving():
    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = get_user_id_by_username(session["username"])

        if user_id:
            services.saving_service.insert_saving(user_id, category, amount)
            flash("Saving added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add saving")
        return redirect(url_for('index'))


@app.route("/add_budget", methods=["POST"])
def add_budget():
    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    if check_session():
        user_id = get_user_id_by_username(session["username"])

        if user_id:
            services.budget_service.insert_budget(user_id, category, amount)
            flash("Budget added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add budget")
        return redirect(url_for('index'))


@app.route("/add_goal", methods=["POST"])
def add_goal():
    goal_name = request.form.get("name")
    category = request.form.get("category")
    goal_amount = float(request.form.get("amount"))
    target_date = request.form.get("date")

    if check_session():
        user_id = get_user_id_by_username(session["username"])

        if user_id:

            if not services.goal_service.is_goal_name_unique(user_id, goal_name):
                flash("Goal name already exists. Please choose an unique name.")
                return redirect(url_for('dashboard'))

            services.goal_service.insert_goal(
                user_id, goal_name, category, goal_amount, target_date)
            flash("Financial goal added successfully")
            return redirect(url_for('dashboard'))

    else:
        flash("Please log in to add financial goal")
        return redirect(url_for('index'))
