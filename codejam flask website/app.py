## importing important and neccerry modules
from datetime import timezone
from operator import methodcaller
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload
from sqlalchemy.sql.functions import ReturnTypeFromArgs, user
from werkzeug.utils import redirect
from flask.helpers import url_for
from sqlalchemy.sql import func
from os import path
import json

## flask initialization
app = Flask(__name__)

## important database initializations and variables
db = SQLAlchemy()
DB_NAME = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ DB_NAME }"
app.config["SECRET_KEY"] = "dkoapf sfksldknfs iodfnsdfos apfdsof"
db.init_app(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    notes = db.relationship("Note")

## flask routes
@app.route("/")
def home():
    if "user" in session:
        return render_template("logged-in-home.html", user=session["user"])
    else:
        return render_template("home.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        signup_username = request.form["signup-username"]
        signup_email = request.form["signup-email"]
        signup_password = request.form["signup-password"]
        signup_confirmed_password = request.form["signup-confirmed-password"]

        signup_user_auth = User.query.filter_by(email=signup_email).first()
        if signup_user_auth:
            flash("Email already exists.", category="error")
        else:
            if len(signup_email) > 4:
                if len(signup_username) > 1:
                    if signup_password == signup_confirmed_password:
                        if len(signup_password) > 7:
                            new_user = User(email=signup_email, password=signup_password, username=signup_username)
                            db.session.add(new_user)
                            db.session.commit()

                            note_data_arr = []
                            for note in range(len(new_user.notes)):
                                note_data_arr.append({"notedata": new_user.notes[note].data, "noteid": new_user.notes[note].id})

                            signup_user_info_dict = {
                                "id": new_user.id,
                                "username": new_user.username,
                                "password": new_user.password,
                                "email": new_user.email,
                                "note_data": note_data_arr
                            }

                            print(signup_user_info_dict["note_data"])

                            session["user"] = signup_user_info_dict
                            return redirect(url_for("home"))
                        else:
                            flash("Password must be atleast 8 characters.", category="error")
                    else:
                        flash("Passwords don't match.", category="error")
                else:
                    flash("Username must be atleast 2 characters.", category="error")
            else:
                flash("Email must be atleast 5 characters")
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_email = request.form["login-email"]
        login_password = request.form["login-password"]

        login_user_auth = User.query.filter_by(email=login_email).first()
        if login_user_auth:
            if login_email == login_user_auth.email and login_password == login_user_auth.password:
                note_data_arr = []
                for note in range(len(login_user_auth.notes)):
                    note_data_arr.append({"notedata": login_user_auth.notes[note].data, "noteid": login_user_auth.notes[note].id})
                
                user_info_dict = {
                    "id": login_user_auth.id,
                    "username": login_user_auth.username,
                    "password": login_user_auth.password,
                    "email": login_user_auth.email,
                    "note_data": note_data_arr
                }

                print(user_info_dict["note_data"])

                session["user"] = user_info_dict
                return redirect(url_for("home"))
            else:
                flash("Invalid password", category="error")
        else:
            flash("Email doesn't exist.", category="error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/developer-tools/code-compiler")
def code_compiler():
    if "user" in session:
        return render_template("coding-compiler.html", user=session["user"])
        code = json.loads(request.data)
    else:
        return redirect(url_for("login"))

@app.route("/developer-tools/stack-overflow")
def stack_overflow():
    if "user" in session:
        return render_template("stack-overflow.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/developer-tools/color-picker")
def color_picker():
    if "user" in session:
        return render_template("color-picker.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/common-tools/notes", methods=["GET","POST"])
def noter():
    if "user" in session:
        all_notes = []
        notes_auth_filter = Note.query.filter_by(user_id=session["user"]["id"])
        if notes_auth_filter:
            for note in notes_auth_filter:
                all_notes.append(note.data)

        session["user"]["note_data"] = all_notes
        if request.method == "POST":
            note = request.form.get("noter-textarea-name")
            print(note)
            if len(note) < 1:
                pass
            else:
                new_note = Note(data=note, user_id=session["user"]["id"])
                db.session.add(new_note)
                db.session.commit()
                all_notes = []
                notes_auth_filter = Note.query.filter_by(user_id=session["user"]["id"])
                if notes_auth_filter:
                    for note in notes_auth_filter:
                        all_notes.append(note.data)
                
                session["user"]["note_data"] = all_notes
                print(session["user"])

        return render_template("noter.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/common-tools/dictionary")
def dictionary():
    if "user" in session:
        return render_template("dictionary.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/common-tools/calculator")
def calculator():
    if "user" in session:
        return render_template("calculator.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/common-tools/timer")
def pomodoro_timer():
    if "user" in session:
        return render_template("timer.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html")

@app.route("/user-notes-data")
def user_notes_data():
    return_str = ""
    for i in range(len(session["user"]["note_data"])):
        return_str += str(session["user"]["note_data"][i]) + ", "
    
    print(session["user"])
    return return_str

## creating a database file
def create_database(app):
    if not path.exists("social media app with flask/" + DB_NAME):
        db.create_all(app=app)
        print("Database Created Successfully!")

create_database(app=app)

## running the flask app
if __name__ == "__main__":
    app.run(debug=True)