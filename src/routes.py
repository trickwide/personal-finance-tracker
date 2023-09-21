from app import app
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from test_db import db
from services.user_service import register_user


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
            return "Passwords do not match", 400

        try:
            register_user(username, password)
            return redirect("/")
        except ValueError as error:
            flash(str(error))

    return render_template("frontend/register.html")
