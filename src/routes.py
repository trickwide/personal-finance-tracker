from app import app
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from test_db import db
from services.user_service import register_user, is_username_valid, is_password_valid


@app.route("/")
def index():
    return render_template("frontend/index.html")


@app.route("/dashboard", methods=["POST"])
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
