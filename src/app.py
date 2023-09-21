from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("frontend/index.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    return render_template("frontend/dashboard.html")


@app.route("/register")
def register():
    return render_template("frontend/register.html")
