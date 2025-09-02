import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps
import requests

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///user.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plan", methods=["GET", "POST"])
def plan():
    if request.method == "POST":
        print(request.form.get("day"))
        db.execute("UPDATE plans SET completed = 1 WHERE user_id = ? and day = ?", session["user_id"], int(request.form.get("day")))
    if db.execute("SELECT * FROM plans WHERE user_id = ?", session["user_id"]):
        datas = db.execute("SELECT * FROM plans WHERE user_id = ?", session["user_id"])
    else:
        return redirect("/form")
    response = requests.get("https://api.alquran.cloud/v1/meta")
    name = response.json()["data"]["surahs"]["references"][datas[0]["surah_num"]-1]["englishName"]
    all_days = db.execute("SELECT day FROM plans WHERE user_id = ? ORDER BY id DESC LIMIT 1", session["user_id"])[0]["day"]

    if db.execute("SELECT day FROM plans WHERE user_id = ? AND completed = 0 ORDER BY id LIMIT 1", session["user_id"]):
        day = db.execute("SELECT day FROM plans WHERE user_id = ? AND completed = 0 ORDER BY id LIMIT 1", session["user_id"])[0]["day"]
        comp = ((day-1)/all_days)*100
        finished = False
    else:
        day = all_days
        comp = 100
        finished = True

    user_name = db.execute("SELECT name from users where id = ?", session["user_id"])[0]["name"]
    print(comp)


    return render_template("plan.html", datas=datas, name = name, day=int(day), comp = comp, all_days = all_days, finished=finished, user_name=user_name)

@app.route("/homepage")
@login_required
def homepage():
    name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])
    return render_template("homepage.html", name = name[0]["name"])

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    session.clear()
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        print(rows)
        print(rows[0]["hash"], request.form.get("password"))
        print(check_password_hash(rows[0]["hash"], request.form.get("password")))
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error =  "Invalid Username and/or Password"
            return render_template("login.html", error = error)
        session["user_id"] = rows[0]["id"]
        return redirect("/homepage")

    else:
        return render_template("login.html", error = error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/form", methods=["GET", "POST"])
def form():
    response = requests.get("https://api.alquran.cloud/v1/meta")
    surahs = response.json()["data"]["surahs"]["references"]

    if request.method == "POST":
        if db.execute("SELECT * FROM plans WHERE user_id = ?", session["user_id"]):
            db.execute("DELETE FROM plans WHERE user_id = ?", session["user_id"])
        print(request.form.get("surah"))
        print(request.form.get("start_ayah"))
        print(request.form.get("ayahs_per_day"))
        apd = int(request.form.get("ayahs_per_day"))
        start = int(request.form.get("start_ayah"))
        total_ayahs = int(response.json()["data"]["surahs"]["references"][int(request.form.get("surah"))-1]["numberOfAyahs"])
        print(total_ayahs)
        days_needed = (total_ayahs + 1 - int(request.form.get("start_ayah"))) // int(request.form.get("ayahs_per_day"))
        if (total_ayahs + 1 - int(request.form.get("start_ayah"))) % int(request.form.get("ayahs_per_day")) != 0:
            days_needed+=1

        plans = []

        for i in range(days_needed):
            plan = {}
            plan["Day"] = i+1
            if i+1!=days_needed:
                plan["Memorise"] = {"surah_number" : int(request.form.get("surah")), "start" : start, "end" : start + apd - 1}
                db.execute("INSERT INTO plans (user_id, day, surah_num, start, end) VALUES (?, ?, ?, ?, ?)", session["user_id"], i+1, int(request.form.get("surah")), start, start + apd - 1)
                start+=apd
            else:
                plan["Memorise"] = {"surah_number" : int(request.form.get("surah")), "start" : start, "end" : total_ayahs }
                db.execute("INSERT INTO plans (user_id, day, surah_num, start, end) VALUES (?, ?, ?, ?, ?)", session["user_id"], i+1, int(request.form.get("surah")), start, total_ayahs)




            plans.append(plan)

        return redirect("/plan")

    return render_template("form.html", surahs=surahs)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("recieved")
        db.execute("INSERT INTO users (email, name, hash) VALUES (?, ?, ?)", request.form.get("email"), request.form.get("name"), generate_password_hash(request.form.get("password")))
        return redirect("/homepage")
    else:
        return render_template("signup.html")

