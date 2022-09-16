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
<<<<<<< Updated upstream
=======
from data_inserter import data_insert
# from flaskext.mysql import MySQL 
# from flask_mysqldb import MySQL
>>>>>>> Stashed changes

import pandas as pd 
from tabula import read_pdf
from pdf_reader import table_extraction, extract_answers, page_info
from tabulate import tabulate
import pandas as pd
import io
<<<<<<< Updated upstream

db.create_all()

@app.route("/")
def home():
    return render_template("index.html")
=======
import os
import mysql.connector
import sys

db.create_all()

table_dict = {1: [("short_summary", "user_id, summary")], 
    3:[("assessment", "user_id, behaviouralAssessment, nonBehaviouralAssessment")], 
    4:[("ba_function", "user_id, description, summary, proposedAlternative")], 
        5: [("goal", "user_id, behaviour, life"), ("strategies", "user_id, environment, teaching, others")], 
    7: [("reinforcement", "user_id, reinforcer, schedule, howIdentified"), ("de_escalation", "user_id, howtoPrompt, strategies, postIncident")]
    } 
>>>>>>> Stashed changes

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all()) #get all the users and pass as objects to value

<<<<<<< Updated upstream
@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    filename = "PBSP Summary Document Final.pdf"
    
    # Read the only the page no.4 of the file
    tables = read_pdf(filename,pages = 4, pandas_options={'header': None},
                         multiple_tables = True, stream = True, lattice=True)

    # Transform the result into a string table format
    table_lists = []
    for table in tables:
        lists = [list(filter(lambda x: x == x, inner_list)) for inner_list in table.values.tolist()] # delete all nan values
        table_lists.append([e for e in lists if e]) #filter out empty lists
    print(table_lists[0])
    subtitle = table_lists[0][0][0]
    answer = table_lists[0][1][0]
    usr = users(subtitle, answer)
    session["user"] = subtitle
    session["email"] = answer
    db.session.add(usr) 
    db.session.commit()
=======
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    # https://www.w3schools.com/Python/python_mysql_insert.asp
    # https://www.educative.io/answers/how-to-add-data-to-databases-in-flask
    data_insert(mydb, cur, "users", "name", ("user1", ))  

    for page_num in [1,3,4,5,7]:
        continuous = page_info[page_num]['continuous']
        next_page = page_info[page_num]['next_page']

        table_lists = table_extraction(page_num)
        answers_all = extract_answers(table_lists)

        if continuous: # continous next page for the same section/attribute
            next_table_lists = table_extraction(page_num+1)
            next_page = next_table_lists[0][0]
            answers_all[-1][0] += str(next_page)
            next_table_lists[0].pop(0) # pop the content that continued from the previous page
        if sum(len(string[1].split(",")) for string in table_dict[page_num]) - len(table_dict[page_num]) > sum(len(i) for i in answers_all):
            if not continuous:
                next_table_lists = table_extraction(page_num+1)
            if page_num+1 == 6: # two lines in that question - concatenate to one
                next_table_lists[0][0][0] = next_table_lists[0][0][0] + next_table_lists[0][1][0]
                next_table_lists[0].pop(1)
            next_answers = extract_answers(next_table_lists)
            next_page = True
    
        table_index = 0
        for db_table, attribute in table_dict[page_num]:
            attr_index = 1
            value = (1,)
            while attr_index < len(answers_all[table_index])+1:
                value += (answers_all[table_index][attr_index-1],)
                attr_index += 1
            next_attr_index = 0
            while next_page and table_index > 0 and next_attr_index < len(next_answers[0]):
                value += (next_answers[0][next_attr_index], )
                next_attr_index += 1
            table_index += 1
            print("db_table", type(db_table))
            print("attribute", type(attribute))
            print("value: ", len(value), value)
            # value = (1, answers[0],answers[1])
            # value = (1, str(answer),)           
            data_insert(mydb, cur, db_table, attribute, value)

>>>>>>> Stashed changes
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
        # flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)