# http://localhost/phpmyadmin/
# from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.sql import text
from config import MysqlConfig, sqliteConfig
from model import users
from exts import db, app
# from flaskext.mysql import MySQL 
# from flask_mysqldb import MySQL

import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io
import os
import mysql.connector
db.create_all()
import sys

def table_extraction(page_num):
    filename = "PBSP Summary Document Final.pdf"

    # Read the only the page no.4 of the file
    tables = read_pdf(filename, pages=page_num, pandas_options={'header': None},
                      multiple_tables=True, stream=True, lattice=True)

    # Transform the result into a string table format
    table_lists = []
    for table in tables:
        lists = [list(filter(lambda x: x == x, inner_list)) for inner_list in
                 table.values.tolist()]  # delete all nan values
        table_lists.append([e for e in lists if e])  # filter out empty lists
    print(table_lists[0])
    return table_lists

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="",
        database="users"
    )
    cur = mydb.cursor()

    table_lists = table_extraction(2)
    # subtitle = table_lists[0][0][0]
    answer = table_lists[0][0]

    db_table = "short_summary"
    attribute = "user_id, summary"
    sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s)"""
    # cur.execute(sql, ("abc",))
    cur.execute(sql, (1, str(answer),))

    mydb.commit()

    return redirect(url_for("view"))

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())  # get all the users and pass as objects to value

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()  # users -the model
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)  # staging
            db.session.commit()  # adding to the db
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:  # have logged in, get it from the session variable
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email  # save the email to the session
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()  # commit user's email
            flash("email is saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:  # haven't logged in or left the browser
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        # flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)