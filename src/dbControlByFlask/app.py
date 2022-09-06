# http://localhost/phpmyadmin/
# from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.sql import text
from config import MysqlConfig, sqliteConfig
from model import users

import pdfminer
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

app = Flask(__name__)
app.secret_key = "abc"
app.config.from_object(MysqlConfig)
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all()) #get all the users and pass as objects to value

@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    output_string = StringIO()
    with open('PBSP.pdf', 'rb') as fin:
        extract_text_to_fp(fin, output_string, laparams=LAParams(),output_type='html', codec=None)

    output = output_string.getvalue().strip()
    user = output[:15] 
    usr = users(user, "")
    session["text"] = user
    db.session.add(usr) 

    user2 =  output[:5] 
    usr2 = users(user2, "")
    session["text2"] = user2
    db.session.add(usr2) 
    db.session.commit()
    return redirect(url_for("view"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first() #users -the model
        if found_user:
            session["email"] = found_user.email      
        else: 
            usr = users(user, "")
            db.session.add(usr) #staging
            db.session.commit() #adding to the db
        return redirect(url_for("user"))
    else: 
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session: # have logged in, get it from the session variable
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email #save the email to the session
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit() #commit user's email
            flash("email is saved")
        else:
            if "email" in session: 
                email = session["email"]
        return render_template("user.html", email=email)
    else: # haven't logged in or left the browser
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)