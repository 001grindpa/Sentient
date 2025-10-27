from flask import Flask, session, render_template, redirect, request, url_for, jsonify
from flask_session import Session
from cs50 import SQL
import httpx
import os
from dotenv import load_dotenv
from random import randint
load_dotenv()

db = SQL("sqlite:///r2-w3.db")

app = Flask(__name__)
api_key = os.getenv("FIREWORKS_API_KEY")

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
        3: "let's hit the road running haha.", 4: "how can I assist you?",
        5: "I'm R2, can't wait to work with you.", 6: "let's talk about that web3 stuff."
        }
    msg = start[n]

    return render_template("index.html", page_id = "index", msg = msg)

@app.route("/assist1", methods=["POST", "GET"])
def assist1():
    if request.method == "POST":
        query = request.json["query"]
        # query = request.form.get("q")
        messages = [{"role": "user", 
                     "content": f"Your name is R2-W3 aka R2, created by Anyanwu Francis aka Grindpa or 0xGrindpa, your creators twitter(x) handle is <a href='https://x.com/0xGrindpa'>creator</a> (you don't need to introduce yourself unless told to. If you're greeted, reply to greetings well, don't say 'affirmative'. The user's name is {session.get("username")}, the current page footer contains text that tells the user you're in beta and can't remember conversations, tell user to read that information at the footer when they raise related complaints). You're a super intelligent DeFi and blockchain research Agent that focuses on getting a project's live statistics(socials, live data, whitepaper etc), answer clearly in less than 20 words and try to keep the conversation DeFi related\n{query}"
                     }]

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        payload = {"model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
                   "messages": messages,
                   "max_tokens": 150,
                   }
        
        r = httpx.post("https://api.fireworks.ai/inference/v1/chat/completions", headers=headers, json=payload)
        
        data = r.json()
        print(data["choices"][0]["message"]["content"])
        return jsonify({"msg": data["choices"][0]["message"]["content"]})

@app.route("/assist2", methods=["POST", "GET"])
def assist2():
    if request.method == "POST":
        query = request.json["query"]

        messages2 = [{
            "role": "user",
            "content": f"strict instructions: check if my query contains a crypto project's name or project ticker, if true, your job is to return in html code, the project's name, about, website, whitepaper link and twitter follower count only in a very concise and brief response in the format 'Name: content.<p>About: content.<p>Website: content.<p>Whitepaper Link: content.<p>Twitter: content.', do not say anything afterwards. if query does not contain any crypto project's name reply '' \n query: {query}"
        }]

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        payload2 = {"model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
                   "messages": messages2,
                   "max_tokens": 150,
                   }
        
        r2 = httpx.post("https://api.fireworks.ai/inference/v1/chat/completions", headers=headers, json=payload2)

        data = r2.json()

        print(data["choices"][0]["message"]["content"])
        return jsonify({"msg": data["choices"][0]["message"]["content"]})

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