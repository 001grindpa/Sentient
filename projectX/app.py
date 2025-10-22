from flask import Flask, session, render_template, redirect, request, url_for, jsonify
from flask_session import Session
from cs50 import SQL

db = SQL("sqlite:///r2-w3.db")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect("/landing")
    return render_template("index.html", page_id = "index")

@app.route("/landing")
def landing():
    return render_template("landing.html", page_id = "landing")

@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = db.execute("SELECT * FROM userData")
        for data in user_data:
            if data.get("username") == username and data.get("password") == password:
                session["username"] = username
                session["passwword"] = password
                return redirect("/")
        return jsonify({"msg": "This account does not exist, please click 'sign up' to create an account"})
    return render_template("login.html", page_id="login")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = db.execute("SELECT * FROM userData")
        for data in user_data:
            if data.get("username") == username and data.get("password") == password:
                return jsonify({"msg": "This account already exits, click 'Log in' to access your account"})
        return redirect("/")
    return render_template("signup.html", page_id="signup-page")



if __name__ == "__main__":
    app.run(port=8000)