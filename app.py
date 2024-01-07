import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import  login_required, getWeather
from flask_mail import Mail, Message


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


mail = Mail()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nail@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)


def send_message(message):
    msg = Message(subject = message.get("subject"), sender = message.get("email"),
            recipients = ["mail@gmail.com"],
            body= message.get("message"), cc = [message.get("email")]
    )
    mail.send(msg)

db = SQL("sqlite:///chegaae.db")

image = [{"id": "0", "title":"Igreja de Nossa Senhora do Rosário e São Benedito","img":"static/rosario.svg","txt":"static/rosario.txt"}, {"id": "1","title":"Museum of Mato Grosso's Natural History (Casa Dom Aquino)","img":"static/casadomaquino.svg", "txt":"static/casadomaquino.txt"}, {"id": "2","title":"Marco Zero", "img":"static/marcozero.svg", "txt":"static/marcozero.txt"}]
random.seed(10)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    global image
    n = random.randrange(0, 3, 1)
    return render_template("home.html", randomimage = image[n]["img"])

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message = "must provide username", number = 403)

        elif not request.form.get("password"):
            return render_template("error.html", message = "must provide password", number = 403)

        username = request.form.get("username")
        username.lower()
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("error.html", message = "invalid username and/or password", number = 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/weather", methods=["GET"])
def weather():
    weather = getWeather()
    if weather:
        location = weather["location"]
        current = weather["current"]
        condition = current["condition"]
        return render_template("weather.html", location = location, current = current, condition = condition)
    else:
        return render_template("error.html", number = 400, message = "Bad request")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST" :
        send_message(request.form)
        return render_template("contact.html", flag = 1 )
    else :
        return render_template("contact.html")


@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    if request.method == "POST":
        idtopic = request.form.get("idtopic")
        check =  db.execute("SELECT users.id AS iduser FROM topic INNER JOIN users ON topic.idUser = users.id WHERE topic.id = ?;", idtopic)
        if check[0]["iduser"] == session["user_id"]:
            db.execute("DELETE FROM comment WHERE idTopic = ?", idtopic)
            db.execute("DELETE FROM topic WHERE id = ?", idtopic)
    topics = db.execute("SELECT topic.id AS id, users.id AS iduser, username, subject, date, text FROM topic INNER JOIN users ON topic.idUser = users.id ORDER BY topic.date DESC;")
    return render_template("forum.html", topics = topics)

@app.route("/newtopic", methods=["GET", "POST"])
@login_required
def newtopic():
    if request.method == "POST":
        subject = request.form.get("subject")
        main = request.form.get("main")
        idUser =  session["user_id"]
        now = datetime.now()
        db.execute("INSERT INTO topic(idUser, subject, text, date) values(?, ?, ?, ?);", idUser, main, subject, now)
        return redirect("/forum")
    else:
        return render_template("newtopic.html")

@app.route("/viewtopic", methods=["GET", "POST"])
@login_required
def viewtopic():
    if request.method == "POST":
        idtopic = request.form.get("idtopic")
        if "comment" in request.form:
            comment = request.form.get("comment")
            now = datetime.now()
            idUser =  session["user_id"]
            db.execute("INSERT INTO comment(idTopic,idUser, text, date) values(?, ?, ?, ?);", idtopic, idUser, comment, now)
        if "exc" in request.form:
            idcomment = request.form.get("idcomment")
            check =  db.execute("SELECT users.id AS iduser FROM comment INNER JOIN users ON comment.idUser = users.id WHERE comment.id = ?;", idcomment)
            if check[0]["iduser"] == session["user_id"]:
                db.execute("DELETE FROM comment WHERE id = ?", idcomment)
        topic = db.execute("SELECT topic.id AS id, username, subject, date, text FROM topic INNER JOIN users ON topic.idUser = users.id WHERE topic.id = ?;", idtopic)
        comments = db.execute("SELECT users.id AS iduser, comment.id AS id, username, comment.date, comment.text FROM comment INNER JOIN topic ON topic.id = comment.idtopic JOIN users ON users.id = comment.iduser WHERE topic.id = ? ORDER BY comment.date DESC;", idtopic)
        return render_template("viewtopic.html", topic = topic[0], comments = comments)
    else:
       return redirect ("/forum")

@app.route("/places", methods=["GET", "POST"])
def places():
    global image
    if request.method == "POST":
        place = request.form
        file  = open(place["txt"], 'r')
        text  = file.read()
        return render_template("place.html", text = text, place = image[int(request.form.get("id"))])
    return render_template("places.html", places = image )

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        check = request.form.get("confirmation")
        if not (username and password and check):
            return render_templete("error.html", message = "Complete all fields", error = 400)
        if check != password:
            return render_template("error.html")
        username.lower()
        checkUsername = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(checkUsername) == 1:
            return render_templete("error.html", message = "Username already exists", error = 400)
        password = generate_password_hash(password, method="pbkdf2", salt_length=16)
        db.execute("INSERT INTO users(username, hash) values(?,?)", username, password)
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/error")
def error():
    return render_template("error.html")


