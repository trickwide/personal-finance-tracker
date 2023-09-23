from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from services.user_service import register_user, is_username_valid, is_password_valid, validate_user_credentials, get_user_id_by_username
from test_db import db
from services.income_service import insert_income, get_total_income, get_income_past_week, get_income_past_month, get_income_past_year


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
            total_income = get_total_income(user_id)
            income_past_week = get_income_past_week(user_id)
            income_past_month = get_income_past_month(user_id)
            income_past_year = get_income_past_year(user_id)
            return render_template("frontend/dashboard.html", total_income=total_income, income_past_week=income_past_week, income_past_month=income_past_month, income_past_year=income_past_year)

    return render_template("frontend/dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # Check if passwords match
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
