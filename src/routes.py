from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from services.user_service import register_user, is_username_valid, is_password_valid, validate_user_credentials, get_user_id_by_username
from db import db
from services.income_service import insert_income, get_total_income, get_income_past_week, get_income_past_month, get_income_past_year
import services.expense_service
import services.saving_service


def check_session():
    return "username" in session


@app.route("/", methods=["GET", "POST"])
def index():
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

            return render_template("frontend/dashboard.html", income=income_data, expense=expense_data, savings=savings_data)

    return render_template("frontend/dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
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
    amount = request.form.get("amount")

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
