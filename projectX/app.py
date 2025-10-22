from flask import Flask, session, render_template, redirect, request, url_for
from flask_session import Session
from cs50 import SQL

db = SQL("sqlite:///r2-w3.db")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("launch"):
        return redirect("/landing")
    return render_template("index.html", page_id = "index")

@app.route("/landing")
def landing():
    return render_template("landing.html", page_id = "landing")

if __name__ == "__main__":
    app.run(port=8080)