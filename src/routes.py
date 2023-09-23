from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from services.user_service import register_user, is_username_valid, is_password_valid, validate_user_credentials
from test_db import db
from services.income_service import insert_income


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

        if not is_username_valid(username):
            flash("Username is too short. Minimum length is 5 characters")
            return redirect(url_for('register'))
        if not is_password_valid(password):
            flash("Password is too weak. It must be at least 8 characters long and contain an uppercase letter, a number and a special character")
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

    if "username" in session:
        user = db.session.execute(text("SELECT user_id FROM users WHERE username = :username"), {
                                  "username": session["username"]}).fetchone()

        if user:
            insert_income(user.user_id, source, amount)
            flash("Income added successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("User not found!")
            return redirect(url_for('index'))

    else:
        flash("Please log in to add income")
        return redirect(url_for('index'))
