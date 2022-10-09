# http://localhost/phpmyadmin/
# from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.sql import text
# from config import MysqlConfig, sqliteConfig
from model import Users, Assessment,Shortsummary, Bafunction, Goal, Strategies, Reinforcement, Deescalation
from exts import db, app

from pdf_reader import table_extraction, extract_answers, page_info
from data_inserter import data_insert

import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io
import os
import mysql.connector

from sqlalchemy import create_engine, inspect

table_dict = {1: [("Shortsummary", "user_id, summary")], 
    3:[("assessment", "user_id, behaviouralAssessment, nonBehaviouralAssessment")], 
    4:[("bafunction", "user_id, description, summary, proposedAlternative")], 
        5: [("goal", "user_id, behaviour, life"), ("strategies", "user_id, environment, teaching, others")], 
    7: [("reinforcement", "user_id, reinforcer, schedule, howIdentified"), ("deescalation", "user_id, howtoPrompt, strategies, postIncident")]
    } 
#mydb = pymysql.connect(  
mydb = mysql.connector.connect(
        user = 'b07a134d14b738',
        host = 'us-cdbr-east-06.cleardb.net',
        password = 'e9e9c4c8',
        database = 'heroku_7fff4db897f6863'
        # connect_timeout=1000
        # wait_timeout=28800 ,
        #
     )
# mydb = mysql.connector.connect(
#         host="localhost", 
#         user="root", 
#         password="",
#         database="users"
#     )
cur = mydb.cursor()
# cur.execute('SET GLOBAL max_allowed_packet=67108864')
# cur.execute('''CREATE TABLE users (id INTEGER, name VARCHAR(20)) ''')
# cur.execute('''CREATE TABLE shortsummary (id INTEGER, summary VARCHAR(1000)) ''')
#cur.execute('''CREATE TABLE assessment (user_id INTEGER, behaviouralAssessment VARCHAR(1000), nonBehaviouralAssessment VARCHAR(1000)) ''')
# cur.execute('''CREATE TABLE bafunction (user_id INTEGER, description VARCHAR(1000), summary VARCHAR(1000),proposedAlternative VARCHAR(1000)) ''')
# cur.execute('''CREATE TABLE goal (user_id INTEGER, behaviour VARCHAR(1000), life VARCHAR(1000)) ''')
# cur.execute('''CREATE TABLE strategies (user_id INTEGER, environment VARCHAR(1000), teaching VARCHAR(1000), others VARCHAR(1000)) ''')
# cur.execute('''CREATE TABLE reinforcement (user_id INTEGER, reinforcer VARCHAR(1000), schedule VARCHAR(1000), howIdentified VARCHAR(1000)) ''')
# cur.execute('''CREATE TABLE deescalation (user_id INTEGER, howtoPrompt VARCHAR(1000), strategies VARCHAR(1000), postIncident VARCHAR(1000)) ''')
# # mysql --host=us-cdbr-east-06.cleardb.net --user=b07a134d14b738 --password=e9e9c4c8 --reconnect heroku_7fff4db897f6863 < schema.sql
#Users.__table__.create(db.session.bind) #working
#Shortsummary.__table__.create(db.session.bind)
#db.Model.__table__.create(db.session.bind) #not working
#Users.create(db, checkfirst=True)
#Shortsummary.create(db, checkfirst=True)
 # can't create all the tables initially as foreign keys are associated, 
# i.e. short_summary's foreign key (user id) doesn't exist in users table yet when creating short_summary table

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    engine = create_engine('mysql://b07a134d14b738:e9e9c4c8@us-cdbr-east-06.cleardb.net/heroku_7fff4db897f6863')
    inspector=inspect(engine)
    print(inspector.has_table('user'))
    if inspector.has_table('user') == False: # if tables haven't created yet, create all tables based on db.model
        db.create_all()
    # https://www.w3schools.com/Python/python_mysql_insert.asp
    # https://www.educative.io/answers/how-to-add-data-to-databases-in-flask
    data_insert(mydb, cur, "users", "name", ("user1", ))  
    
    user = Users.query.filter(Users.name == "user1").first() # get user id for other tables' user id foreign key
    print(user.id)
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
            value = (user.id,)
            while attr_index < len(answers_all[table_index])+1:
                value += (answers_all[table_index][attr_index-1],)
                attr_index += 1
            next_attr_index = 0
            while next_page and table_index > 0 and next_attr_index < len(next_answers[0]):
                value += (next_answers[0][next_attr_index], )
                next_attr_index += 1
            table_index += 1
            print("value: ", len(value), value)
            # value = (1, answers[0],answers[1])
            # value = (1, str(answer),)

            data_insert(mydb, cur, db_table, attribute, value)
    # cur.close()
    # db.session.close()
    return "successful"
    return redirect(url_for("view"))


@app.route("/view")
def view():
    # https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
    # https://stackoverflow.com/questions/18150144/how-to-query-a-database-after-render-template
    # cur.execute("SELECT * FROM short_summary")
    # data = cur.fetchall()
    # return render_template("view.html", data=data)
    users_table = Users.query.all()
    short_summary_table = Shortsummary.query.all()
    assessment_table = Assessment.query.all()
    ba_function_table = Bafunction.query.all()
    goal_table = Goal.query.all()
    strategies_table = Strategies.query.all()
    reinforcement_table = Reinforcement.query.all()
    de_escalation_table = Deescalation.query.all()
    cur.close()
    db.session.close()
    return render_template("view.html", users_table=users_table, short_summary_table=short_summary_table, 
    assessment_table=assessment_table, ba_function_table=ba_function_table, goal_table=goal_table, 
    strategies_table=strategies_table, reinforcement_table=reinforcement_table, de_escalation_table=de_escalation_table)
    # return render_template("view.html", values=users.query.all())  # get all the users and pass as objects to value

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         # session.permanent = True
#         user = request.form["nm"]
#         session["user"] = user

#         found_user = Users.query.filter_by(name=user).first()  # users -the model
#         if found_user:
#             session["email"] = found_user.email
#         else:
#             usr = Users(user, "")
#             db.session.add(usr)  # staging
#             db.session.commit()  # adding to the db
#         return redirect(url_for("user"))
#     else:
#         if "user" in session:
#             return redirect(url_for("user"))
#         return render_template("login.html")


# @app.route("/user", methods=["POST", "GET"])
# def user():
#     email = None
#     if "user" in session:  # have logged in, get it from the session variable
#         user = session["user"]

#         if request.method == "POST":
#             email = request.form["email"]
#             session["email"] = email  # save the email to the session
#             found_user = Users.query.filter_by(name=user).first()
#             found_user.email = email
#             db.session.commit()  # commit user's email
#             flash("email is saved")
#         else:
#             if "email" in session:
#                 email = session["email"]
#         return render_template("user.html", email=email)
#     else:  # haven't logged in or left the browser
#         flash("You are not logged in")
#         return redirect(url_for("login"))


# @app.route("/logout")
# def logout():
#     if "user" in session:
#         user = session["user"]
#         # flash(f"You have been logged out, {user}", "info")
#     session.pop("user", None)
#     session.pop("email", None)
#     return redirect(url_for("login"))

