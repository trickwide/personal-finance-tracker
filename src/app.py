from os import getenv
from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("frontend/index.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    return render_template("frontend/dashboard.html")


@app.route("/register")
def register():
    return render_template("frontend/register.html")
