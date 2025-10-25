from flask import Flask, session, render_template, redirect, request, url_for, jsonify
from flask_session import Session
from cs50 import SQL
import requests
import ulid
from random import randint

db = SQL("sqlite:///r2-w3.db")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect("/landing")
    n = randint(1, 6)
    start = {
        1: "what's on your mind?", 2: "how do we start off?",
        3: "let's hit the road running haha.", 4: "how can i assist you?",
        5: "i'm R2, can't wait to work with you.", 6: "let's talk about that web3 stuff."
        }
    msg = start[n]

    return render_template("index.html", page_id = "index", msg = msg)

@app.route("/assist", methods=["POST", "GET"])
def assist():
    if request.method == "POST":
        query = request.json["query"]
        # query = request.form.get("q")
        response = requests.post("http://127.0.0.1:8080/assist",
            json={
                "query": {
                    "id": str(ulid.new()),
                    "prompt": query
                },
                "session": {
                    "id": session.get("username"),
                    "processor_id": "default",
                    "activity_id": str(ulid.new()),
                    "request_id": str(ulid.new()),
                    "interactions": []
                }
            },
            headers={
            "Content-Type": "application/json"
            })
        
        print(response.text)
        # print(query)
        return jsonify(response.json())

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
                return redirect("/")
        return jsonify({"msg": "This account does not exist, please click 'sign up' to create an account"})
    return render_template("login.html", page_id="login")

@app.route("/loginCheck", methods=["POST", "GET"])
def loginCheck():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = db.execute("SELECT * FROM userData")
        for data in user_data:
            if data.get("username") == username and data.get("password") == password:
                return jsonify({"msg": "nothing"})
        return jsonify({"msg": "This account does not exist, please click 'sign up' to create an account"})

@app.route("/logout")
def logout():
    session["username"] = None
    session["password"] = None
    return redirect("/login")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        user_data = db.execute("SELECT * FROM userData")
        for data in user_data:
            if data.get("username") == username:
                return jsonify({"msg": "This username is not available"})
            if data.get("username") == username and data.get("password") == password:
                return jsonify({"msg": "This account already exits, click 'Log in' below to access your account"})

        if password == password_confirm:
            db.execute("INSERT INTO userData(username, password) VALUES(?, ?)", username, password)
            session["username"] = username
            session["password"] = password
            return redirect("/")
    return render_template("signup.html", page_id="signup-page")

@app.route("/signupCheck", methods=["GET", "POST"])
def signupCheck():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        user_data = db.execute("SELECT * FROM userData")
        for data in user_data:
            if data.get("username") == username:
                return jsonify({"msg": "This username is not available"})
            if data.get("username") == username and data.get("password") == password:
                return jsonify({"msg": "This account already exits, click 'Log in' below to access your account"})
        if password != password_confirm:
            return jsonify({"msg": "Password mismatched"})
        elif password == password_confirm and password != "":
            return jsonify({"msg": "Valid match"})
        return jsonify({"msg": "nothing"})
    
@app.route("/test")
def test():
    name = request.args.get("q")
    return jsonify({"msg": f"Hello {name}, nice to meet you"})

if __name__ == "__main__":
    app.run(port=8000)