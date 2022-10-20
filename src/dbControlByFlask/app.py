# http://localhost/phpmyadmin/
# from django.shortcuts import render
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.sql import text
from config import MysqlConfig, sqliteConfig
from model import users, Assessment, ShortSummary, BAFunction, Goal, Strategies, Reinforcement, DeEscalation
from exts import db, app
# from flaskext.mysql import MySQL
# from flask_mysqldb import MySQL
import read_db
import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import io
import os
import mysql.connector
import pdfExtraction2 as extract
from data_inserter import data_insert, data_get_last_id, data_get_last_id_by_intervention
from read_db import getAll
from werkzeug.utils import secure_filename

db.create_all()
import sys

table_dict = {
    1: [("short_summary", "user_id, summary")],
    3: [("assessment",
         "user_id, behaviouralAssessment, nonBehaviouralAssessment")],
    4: [("ba_function", "user_id, description, summary, proposedAlternative")],
    5: [("goal", "user_id, behaviour, life"),
        ("strategies", "user_id, environment, teaching, others")],
    7: [("reinforcement", "user_id, reinforcer, schedule, howIdentified"),
        ("de_escalation", "user_id, howtoPrompt, strategies, postIncident")]
}
page_info = {
    1: {
        "continuous": False,
        "next_page": True
    },
    3: {
        "continuous": False,
        "next_page": False
    },
    4: {
        "continuous": False,
        "next_page": False
    },
    5: {
        "continuous": True,
        "next_page": True
    },
    7: {
        "continuous": False,
        "next_page": True
    }
}

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               database="users")
cur = mydb.cursor()

user_id = 0

current_pdf = None

def table_extraction(page_num):
    filename = "PBSP Summary Document (Draft V3 MV 170822) - QLD Model Plan - No Comments.pdf"

    # Read the only the page no.4 of the file
    tables = read_pdf(filename,
                      pages=page_num,
                      pandas_options={'header': None},
                      multiple_tables=True,
                      stream=True,
                      lattice=True,
                      encoding='latin1')
    print("!!!!!!!!!!!!!!!--", page_num, "--!!!!!!!!!!!!!!!!!!")
    print(tables)
    # Transform the result into a string table format
    table_lists = []
    for table in tables:
        lists = [
            list(filter(lambda x: x == x, inner_list))
            for inner_list in table.values.tolist()
        ]  # delete all nan values
        table_lists.append([e for e in lists if e])  # filter out empty lists
    print(table_lists[0])
    return table_lists


def extract_answers(table_lists):
    answers_all = []
    for table in table_lists:
        i = 1
        answers = []
        while i < len(table):
            if len(table[i - 1]) == 1 and len(table[i]) == 1:
                answers.append(str(table[i]))
                # print(table[i]) #first index: how many tables in that page
                i += 1
            else:
                if len(table) == 2:  #sub-col name - value
                    # insert the value as attribute directly
                    print("aaa")
                else:
                    # insert to another table
                    print("bbb", table[i])
            i += 1
        if len(answers) != 0:
            answers_all.append(answers)
    return answers_all


@app.route("/")
def home():
    return render_template("index.html")




@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    sql = """INSERT INTO users ( name ) VALUES ("user1")"""
    cur.execute(sql)
    mydb.commit()

    for page_num in [1, 3, 4, 5, 7]:
        continuous = page_info[page_num]['continuous']
        next_page = page_info[page_num]['next_page']

        table_lists = table_extraction(page_num)
        answers_all = extract_answers(table_lists)

        if continuous:  # continous next page for the same section/attribute
            next_table_lists = table_extraction(page_num + 1)
            next_page = next_table_lists[0][0]
            answers_all[-1][0] += str(next_page)
            next_table_lists[0].pop(
                0)  # pop the content that continued from the previous page
        if sum(len(string[1].split(","))
               for string in table_dict[page_num]) - len(
                   table_dict[page_num]) > sum(len(i) for i in answers_all):
            if not continuous:
                next_table_lists = table_extraction(page_num + 1)
            if page_num + 1 == 6:  # two lines in that question - concatenate to one
                next_table_lists[0][0][
                    0] = next_table_lists[0][0][0] + next_table_lists[0][1][0]
                next_table_lists[0].pop(1)
            next_answers = extract_answers(next_table_lists)
            next_page = True

        table_index = 0
        for db_table, attribute in table_dict[page_num]:
            attr_index = 1
            value = (1, )
            while attr_index < len(answers_all[table_index]) + 1:
                value += (answers_all[table_index][attr_index - 1], )
                attr_index += 1
            next_attr_index = 0
            while next_page and table_index > 0 and next_attr_index < len(
                    next_answers[0]):
                value += (next_answers[0][next_attr_index], )
                next_attr_index += 1
            table_index += 1
            print("value: ", len(value), value)
            # value = (1, answers[0],answers[1])
            # value = (1, str(answer),)
            if len(attribute.split()) == 2:
                sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s)"""
            elif len(attribute.split()) == 3:
                sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s, %s)"""
            elif len(attribute.split()) == 4:
                sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s, %s, %s)"""
            elif len(attribute.split()) == 5:
                sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s, %s, %s, %s)"""
            elif len(attribute.split()) == 6:
                sql = """INSERT INTO """ + db_table + """(""" + attribute + """) VALUES (%s, %s, %s, %s, %s, %s)"""
            # cur.execute(sql, ("abc",))
            print(sql)
            cur.execute(sql, value)

    mydb.commit()

    return redirect(url_for("view"))


@app.route("/view")
def view():
    # https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
    # https://stackoverflow.com/questions/18150144/how-to-query-a-database-after-render-template
    # cur.execute("SELECT * FROM short_summary")
    # data = cur.fetchall()
    # return render_template("view.html", data=data)
    users_table = users.query.all()
    short_summary_table = ShortSummary.query.all()
    assessment_table = Assessment.query.all()
    ba_function_table = BAFunction.query.all()
    goal_table = Goal.query.all()
    strategies_table = Strategies.query.all()
    reinforcement_table = Reinforcement.query.all()
    de_escalation_table = DeEscalation.query.all()
    return render_template("view.html",
                           users_table=users_table,
                           short_summary_table=short_summary_table,
                           assessment_table=assessment_table,
                           ba_function_table=ba_function_table,
                           goal_table=goal_table,
                           strategies_table=strategies_table,
                           reinforcement_table=reinforcement_table,
                           de_escalation_table=de_escalation_table)
    # return render_template("view.html", values=users.query.all())  # get all the users and pass as objects to value

@app.route("/upload")
def upload():

    user = session.get("user")
    found_user = users.query.filter_by(
        name=user).first()
    print(found_user)
    global user_id
    user_id = found_user.id
    return render_template('upload.html')


@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        global current_pdf
        current_pdf = request.files['file']
        #print(request.files)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        #return 'file uploaded successfully'
        return redirect(url_for("process_pdf2"))
    else:

        return render_template('upload.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(
            name=user).first()  # users -the model
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
            return redirect(url_for("upload"))
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


@app.route("/getUserInfo/<id>", methods=["POST", "GET"])
def get_user_information(id):
    user_id = int(id)
    return getAll(cur, mydb, user_id)


@app.route("/process2", methods=["GET", "POST"])
def process_pdf2():

    #file_name = "PBSP Summary Document (Draft V3 MV 170822) - QLD Model Plan - No Comments.pdf"
    current_bold_position = 0
    current_table_position = 0
    current_text_position = 0
# Page1
    dict_pdf, all_content, tables, bolds = extract.get_pdf_content(current_pdf.filename)
    current_content = extract.extract_paragraph(
        "Provide a short summary about the person with disability who is the focus of the PBSP",
        "PAGE 2 – Assessments and Data Gathering", all_content)
    data_insert(mydb, cur, "short_summary", ("user_id, " + "summary"),
                (user_id, current_content))

# Page2
    behavioural_assessment = extract.extract_paragraph(
        "Outline the behavioural assessment approaches implemented to develop this PBSP",
        "Additional non-behavioural assessments undertaken or reviewed to inform the development of this PBSP",
        all_content)
    non_behavioural_assessment = extract.extract_paragraph(
        "Additional non-behavioural assessments undertaken or reviewed to inform the development of this PBSP",
        "PAGE 3 – Functional Behavioural Assessment", all_content)
    #stor the unique information in assessment table
    data_insert(
        mydb, cur, "assessment",
        ("user_id, " + "behaviouralAssessment, " + "nonBehaviouralAssessment"),
        (user_id, behavioural_assessment, non_behavioural_assessment))

    #get the latest assessment_id by given user_id
    last_id = data_get_last_id(mydb, cur, "assessment", user_id)[0][0]
    current_table = extract.extract_table(
        'Persons consulted to prepare this PBSP (add/remove rows as required)',
        'Outline the behavioural assessment approaches implemented to develop this PBSP',
        tables, current_table_position)

    current_table_position = current_table[1]
    for temp in current_table[0]:
        data_insert(mydb, cur, "persons_consulted",
                    ("who, " + "how, " + "assessment_id"),
                    (tuple(temp + [last_id])))
    #.................................................................
    list_function = [
        'Avoidance/escape', 'Communication', 'Physical/sensory  need',
        'Access –  person/object/activity', 'Other – please  specify'
    ]
    function_name = []
    for i in list_function:
        for j in bolds:
            if i in j:
                function_name.append(i)
    descrip_behaviours = extract.extract_paragraph(
        "Description of behaviours (include frequency, duration and severity) that align with this function",
        "etting events, triggers and consequences related to these behaviours (add/remove rows as necessary)",
        all_content)

    summary = extract.extract_paragraph(
        "A summary statement outlining the functional hypothesis",
        "Proposed alternative or functionally equivalent replacement behaviour(s)",
        all_content)
    proposed_alternative = extract.extract_paragraph(
        "Proposed alternative or functionally equivalent replacement behaviour(s)",
        "Page 4 – Positive Behavioural Support Interventions", all_content)
    data_insert(mydb, cur, "ba_function",
                ("user_id, " + "functionName, " + "description, " +
                 "summary, " + "proposedAlternative"),
                (user_id, str(function_name), descrip_behaviours, summary,
                 proposed_alternative))
    last_id = data_get_last_id(mydb, cur, "ba_function", user_id)[0][0]
    print(tables[current_table_position:])
    stc = extract.extract_table(
        'Setting events, triggers and consequences related to these behaviours (add/remove rows as necessary)',
        'A summary statement outlining the functional hypothesis', tables, current_table_position)
    current_table_position = stc[1]
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print(stc)
    for temp in stc[0]:

        data_insert(
            mydb, cur, "stc",
            ("settingEvents, " + "stc.trigger, " + "consequences, " + "f_id"),
            (tuple(temp + [last_id])))

#goal
    goals_behaviours = extract.extract_paragraph(
        "Goal(s) specific to the behaviours described",
        "Goals specific to enhancing the person’s quality of life",
        all_content)
    goals_life = extract.extract_paragraph_given_start(
        "Goals specific to enhancing the person’s quality of life",
        "Strategies", all_content,current_text_position)
    current_text_position = goals_life[1]
    data_insert(mydb, cur, "goal", ("user_id, " + "behaviour, " + "life"),
                (user_id, goals_behaviours, goals_life[0]))

#strategy
    environmental = extract.extract_paragraph_given_start(
        "Environmental changes to address setting events and triggers (changes to reduce and/or eliminate their influence)",
        "Teaching of the alternative or functionally equivalent replacement behaviour(s) (e.g., description of the teaching",
        all_content,current_text_position)
    current_text_position = environmental[1]
    teaching = extract.extract_paragraph_given_start(
        "strategy and materials needed)",
        "Other strategies (e.g., social, independence, coping, tolerance, etc.)",
        all_content,current_text_position)
    current_text_position = teaching[1]
    others = extract.extract_paragraph(
        "Other strategies (e.g., social, independence, coping, tolerance, etc.)",
        "Reinforcement for Skill Development", all_content)
    data_insert(mydb, cur, "strategies",
                ("user_id, " + "environment, " + "teaching, " + "others"),
                (user_id, environmental[0], teaching[0], others))

#reinforcement
    reinforcer = extract.extract_paragraph("Proposed reinforcers",
                                           "Schedule of reinforcement",
                                           all_content)
    schedule = extract.extract_paragraph(
        "Schedule of reinforcement", "How were these reinforcers identified?",
        all_content)
    how_identified = extract.extract_paragraph(
        "How were these reinforcers identified?",
        "De-Escalation - Reactive strategies for challenging behaviours",
        all_content)
    data_insert(
        mydb, cur, "reinforcement",
        ("user_id, " + "reinforcer, " + "schedule, " + "howIdentified"),
        (user_id, reinforcer, schedule, how_identified))

#DeEscalation

    how_prompt = extract.extract_paragraph(
        "How to prompt the alternative or functionally replacement behaviour(s)",
        "Strategies to ensure the safety of the person and/or others",
        all_content)
    strategies = extract.extract_paragraph(
        "Strategies to ensure the safety of the person and/or others",
        "Post-incident debriefing with the person with disability and/or parents, support staff, etc.",
        all_content)
    post_incident = extract.extract_paragraph(
        "Post-incident debriefing with the person with disability and/or parents, support staff, etc.",
        "PAGE 5 – Restrictive Intervention", all_content)
    data_insert(
        mydb, cur, "de_escalation",
        ("user_id, " + "howtoPrompt, " + "strategies, " + "postIncident"),
        (user_id, how_prompt, strategies, post_incident))

    for i in range(len(bolds)):
        if bolds[i].startswith("PAGE 5"):
            temp = bolds[i]
    # if has constraint
    temp = temp.split()
    if "Yes" in temp:
        types = ['Chemical', 'Physical', 'Mechanical', 'Environmental', 'Seclusion']
        stored_types = []
        for i in temp:
            if i in types:
                stored_types.append(i)
        stored_types = str(stored_types)
        data_insert(
            mydb, cur, "intervention",
            ("user_id, " + "type, " + "ifProposed"),
            (user_id, stored_types, "yes"))
        intervention_id = data_get_last_id(mydb, cur, "intervention",
                                   user_id)[0][0]
#chemical
        midication = extract.extract_table(
            'Medication(s) that will be used (e.g., name, dosage, frequency, administration, route, prescriber)',
            'Positive behavioural support strategies to be used before the PRN use of the medication',
            tables, current_table_position)
        current_table_position = midication[1]
        positive_strategies = extract.extract_paragraph(
            "Positive behavioural support strategies to be used before the PRN use of the medication",
            "Circumstance(s) in which the medication(s) will be used",
            all_content)
        circumstance = extract.extract_paragraph(
            "Circumstance(s) in which the medication(s) will be used",
            "Procedure for administering the medication(s), including observation and monitoring of side-effects",
            all_content)
        procedure = extract.extract_paragraph(
            "Procedure for administering the medication(s), including observation and monitoring of side-effects",
            "How will chemical restraint be gradually reduced as behavioural goals are achieved by the person?",
            all_content)
        how_restraint_reduce = extract.extract_paragraph(
            "How will chemical restraint be gradually reduced as behavioural goals are achieved by the person?",
            "Why is the use of this medication the least restrictive way of ensuring the safety of the person and/or others?",
            all_content)
        why = extract.extract_paragraph_given_start(
            "Why is the use of this medication the least restrictive way of ensuring the safety of the person and/or others?",
            "Social validity of the restrictive practice", all_content,
            current_text_position)
        current_text_position = why[1]
        social_validity = extract.extract_table(
            'Social validity of the restrictive practice',
            'Authorisation for the use of restrictive practices', tables,
            current_table_position)
        current_table_position = social_validity[1]
        authorisation = extract.extract_table(
            'Authorisation for the use of restrictive practices',
            'Description of the restraint(s) to be used', tables,
            current_table_position)
        current_table_position = authorisation[1]
        data_insert(
            mydb, cur, "chemical_restraint",
            ("iv_id, " + "positiveStrategy, " + "circumstance, " +
             "chemical_restraint.procedure, " + "howRestrainReduce, " + "why"),
            (intervention_id, positive_strategies, circumstance, procedure,
             how_restraint_reduce, why[0]))
        last_id = data_get_last_id_by_intervention(mydb, cur, "chemical_restraint",
                                   intervention_id)[0][0]
        for temp in midication[0]:
            data_insert(
                mydb, cur, "medication",
                ("name, " + "dosage, " + "frequency, " + "administration, " +
                 "route, " + "prescriber, " + "cr_id"),
                (tuple(temp + [last_id])))
        for temp in social_validity[0]:
            data_insert(mydb, cur, "social_validity1",
                        ("how, " + "who, " + "cr_id"),
                        (tuple(temp + [last_id])))
        for temp in authorisation[0]:
            data_insert(mydb, cur, "authorisation1",
                        ("authorisationBody, " + "approvalPeriod, " + "cr_id"),
                        (tuple(temp + [last_id])))
#physical
        description = extract.extract_paragraph_given_start(
            "Description of the restraint(s) to be used",
            "Positive behavioural support strategies to be used before the use of the restraint",
            all_content, current_text_position)
        current_text_position = description[1]
        positive_behaviour = extract.extract_paragraph_given_start(
            "Positive behavioural support strategies to be used before the use of the restraint",
            "Circumstance(s) in which the restraint will be used", all_content,
            current_text_position)
        current_text_position = positive_behaviour[1]
        circumstance = extract.extract_paragraph_given_start(
            "Circumstance(s) in which the restraint will be used",
            "Procedure for using the restraint, including observation, monitoring and maximum time period",
            all_content, current_text_position)
        current_text_position = circumstance[1]
        procedure = extract.extract_paragraph_given_start(
            "Procedure for using the restraint, including observation, monitoring and maximum time period",
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            all_content, current_text_position)
        current_text_position = procedure[1]
        how = extract.extract_paragraph_given_start(
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            "Why is the use of this restraint the least restrictive way of ensuring the safety of the person and/or others?",
            all_content, current_text_position)
        current_text_position = how[1]
        why = extract.extract_paragraph_given_start(
            "Why is the use of this restraint the least restrictive way of ensuring the safety of the person and/or others?",
            "Social validity of the restrictive practice", all_content,
            current_text_position)
        current_text_position = why[1]
        data_insert(mydb, cur, "physical_restraint",
                    ("iv_id, " + "description, " + "positiveStrategy, " +
                     "circumstance, " + "physical_restraint.procedure, " +
                     "how, " + "why"),
                    (intervention_id, description[0], positive_behaviour[0],
                     circumstance[0], procedure[0], how[0], why[0]))
        social_validity = extract.extract_table(
            'Social validity of the restrictive practice',
            'Authorisation for the use of restrictive practice', tables,
            current_table_position)
        current_table_position = social_validity[1]
        authorisation = extract.extract_table(
            'Authorisation for the use of restrictive practice',
            'Description of the restraint(s) to be used', tables,
            current_table_position)
        current_table_position = authorisation[1]
        last_id = data_get_last_id_by_intervention(mydb, cur, "physical_restraint",
                                   intervention_id)[0][0]

        for temp in social_validity[0]:
            data_insert(mydb, cur, "social_validity2",
                        ("how, " + "who, " + "pr_id"),
                        (tuple(temp + [last_id])))
        for temp in authorisation[0]:
            data_insert(mydb, cur, "authorisation2",
                        ("authorisationBody, " + "approvalPeriod, " + "pr_id"),
                        (tuple(temp + [last_id])))

#mechanical
        description = extract.extract_paragraph_given_start(
            "Description of the restraint(s) to be used", "Frequency of use",
            all_content, current_text_position)
        current_text_position = description[1]
        frequency = None
        for i in range(len(bolds)):
            if 'Routine' in bolds[i]:
                frequency = "Routine use"
                current_bold_position = i + 1
                break
            elif 'needed' in bolds[i]:
                frequency = "As needed"
                current_bold_position = i + 1
                break

        positive_behaviour = extract.extract_paragraph_given_start(
            "Positive behavioural support strategies to be used before the use of the restraint",
            "Circumstance(s) in which the restraint will be used", all_content,
            current_text_position)
        current_text_position = positive_behaviour[1]
        circumstance = extract.extract_paragraph_given_start(
            "Circumstance(s) in which the restraint will be used",
            "Procedure for using the restraint, including observation, monitoring and maximum time period",
            all_content, current_text_position)
        current_text_position = circumstance[1]
        procedure = extract.extract_paragraph_given_start(
            "Procedure for using the restraint, including observation, monitoring and maximum time period",
            "How do you know this restraint is safe to use?", all_content,
            current_text_position)
        current_text_position = procedure[1]
        how_know = extract.extract_paragraph_given_start(
            "How do you know this restraint is safe to use?",
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            all_content, current_text_position)
        current_text_position = how_know[1]
        how_restraint = extract.extract_paragraph_given_start(
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            "Why is the use of this practice the least restrictive way of ensuring the safety of the person and/or others?",
            all_content, current_text_position)
        current_text_position = how_restraint[1]
        why = extract.extract_paragraph_given_start(
            "Why is the use of this restraint the least restrictive way of ensuring the safety of the person and/or others?",
            "Social validity of the practice", all_content,
            current_text_position)
        current_text_position = why[1]
        data_insert(mydb, cur, "mechanical_restraint",
                    ("iv_id, " + "description, " + "frequency, " +
                     "positiveStrategy, " + "circumstance, " +
                     "mechanical_restraint.procedure, " + "howKnow, " + "howRestraint, " + "why"),
                    (intervention_id, description[0], frequency, positive_behaviour[0],
                     circumstance[0], procedure[0], how_know[0], how_restraint[0], why[0]))

        social_validity = extract.extract_table(
            'Social validity of the practice',
            'Authorisation for the use of restrictive practices', tables,
            current_table_position)
        current_table_position = social_validity[1]
        authorisation = extract.extract_table(
            'Authorisation for the use of restrictive practices',
            'Description of the restraint(s) to be used', tables,
            current_table_position)
        current_table_position = authorisation[1]
        last_id = data_get_last_id_by_intervention(mydb, cur, "mechanical_restraint",
                                   intervention_id)[0][0]

        for temp in social_validity[0]:
            data_insert(mydb, cur, "social_validity3",
                        ("how, " + "who, " + "mr_id"),
                        (tuple(temp + [last_id])))
        for temp in authorisation[0]:
            data_insert(mydb, cur, "authorisation3",
                        ("authorisationBody, " + "approvalPeriod, " + "mr_id"),
                        (tuple(temp + [last_id])))
#environmental
        description = extract.extract_paragraph_given_start(
            "Description of the restraint(s) to be used", "Frequency of use",
            all_content, current_text_position)
        current_text_position = description[1]
        frequency = None
        for i in range(current_bold_position, len(bolds)):
            if 'Routine' in bolds[i]:
                frequency = "Routine use"
                current_bold_position = i
                break
            elif 'needed' in bolds[i]:
                frequency = "As needed"
                current_bold_position = i
                break

        positive_behaviour = extract.extract_paragraph_given_start(
            "Positive behavioural support strategies to be used before the as needed use of the restraint",
            "Circumstance(s) in which the restraint will be used", all_content,
            current_text_position)
        current_text_position = positive_behaviour[1]
        circumstance = extract.extract_paragraph_given_start(
            "Circumstance(s) in which the restraint will be used",
            "What is the person with disability prevented from accessing?",
            all_content, current_text_position)
        current_text_position = circumstance[1]
        person = extract.extract_paragraph_given_start(
            "What is the person with disability prevented from accessing?",
            "Procedure for using the restraint, including observation and monitoring",
            all_content, current_text_position)
        current_text_position = person[1]
        procedure = extract.extract_paragraph_given_start(
            "Procedure for using the restraint, including observation and monitoring",
            "Will other people be impacted by the use of this restraint?",
            all_content, current_text_position)
        current_text_position = procedure[1]

        impact = None
        for i in range(current_bold_position, len(bolds)):
            if 'Yes' in bolds[i]:
                impact = "Routine use"
                current_bold_position = i + 1
                break
            elif 'No' in bolds[i]:
                impact = "As needed"
                current_bold_position = i + 1
                break

        how_impact = extract.extract_paragraph_given_start(
            "If YES, how will impact on others be minimised?",
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            all_content, current_text_position)
        current_text_position = how_impact[1]

        how_restraint = extract.extract_paragraph_given_start(
            "How will the restraint be gradually reduced as behavioural goals are achieved by the person?",
            "Why is the use of this practice the least restrictive way of ensuring the safety of the person and/or others?",
            all_content, current_text_position)
        current_text_position = how_restraint[1]

        why = extract.extract_paragraph_given_start(
            "Why is the use of this practice the least restrictive way of ensuring the safety of the person and/or others?",
            "Social validity of the practice", all_content,
            current_text_position)
        current_text_position = why[1]
        data_insert(mydb, cur, "environmental_restraint",
                    ("iv_id, " + "description, " + "frequency, " +
                     "positiveStrategy, " + "circumstance, " + "person, " +
                     "environmental_restraint.procedure, " + "impact, " +
                     "howImpact, " + "howRestraint, " + "why"),
                    (intervention_id, description[0], frequency, positive_behaviour[0],
                     circumstance[0], person[0], procedure[0], impact,
                     how_impact[0], how_restraint[0], why[0]))

        social_validity = extract.extract_table(
            'Social validity of the practice',
            'Authorisation for the use of the practices', tables,
            current_table_position)
        current_table_position = social_validity[1]
        authorisation = extract.extract_table(
            'Authorisation for the use of the practices', 'Frequency of use',
            tables, current_table_position)
        current_table_position = authorisation[1]
        last_id = data_get_last_id_by_intervention(mydb, cur, "environmental_restraint",
                                   intervention_id)[0][0]

        for temp in social_validity[0]:
            data_insert(mydb, cur, "social_validity4",
                        ("how, " + "who, " + "er_id"),
                        (tuple(temp + [last_id])))
        for temp in authorisation[0]:
            data_insert(mydb, cur, "authorisation4",
                        ("authorisationBody, " + "approvalPeriod, " + "er_id"),
                        (tuple(temp + [last_id])))
#Seclusion
        for i in range(current_bold_position, len(bolds)):
            if 'Routine' in bolds[i]:
                frequency = "Routine use"
                current_bold_position = i
                break
            elif 'needed' in bolds[i]:
                frequency = "As needed"
                current_bold_position = i
                break

        positive_strategies = extract.extract_paragraph_given_start(
            "Positive behavioural support strategies to be used before the as needed use of seclusion",
            "Circumstance(s) in which seclusion will be used", all_content,
            current_text_position)
        current_text_position = positive_strategies[1]

        circumstance = extract.extract_paragraph_given_start(
            "Circumstance(s) in which seclusion will be used",
            "The maximum frequency of seclusion per day, week and/or month; and for how long (minutes/hours)",
            all_content, current_text_position)
        current_text_position = circumstance[1]

        max_frequency = extract.extract_paragraph_given_start(
            "The maximum frequency of seclusion per day, week and/or month; and for how long (minutes/hours)",
            "Procedure for using seclusion, including observation and monitoring",
            all_content, current_text_position)
        current_text_position = max_frequency[1]

        procedure = extract.extract_paragraph_given_start(
            "Procedure for using seclusion, including observation and monitoring",
            "How will seclusion be gradually reduced as behavioural goals are achieved by the person?",
            all_content, current_text_position)
        current_text_position = procedure[1]

        how = extract.extract_paragraph_given_start(
            "How will seclusion be gradually reduced as behavioural goals are achieved by the person?",
            "Why is the use seclusion the least restrictive way of ensuring the safety of the person and/or others?",
            all_content, current_text_position)
        current_text_position = how[1]

        why = extract.extract_paragraph_given_start(
            "Why is the use seclusion the least restrictive way of ensuring the safety of the person and/or others?",
            "Social validity of seclusion", all_content, current_text_position)
        current_text_position = why[1]

        data_insert(
            mydb, cur, "seclusion_restraint",
            ("iv_id, " + "frequency, " + "positiveStrategy, " +
             "circumstance, " + "maxFrequency, " +
             "seclusion_restraint.procedure, " + "how, " + "why"),
            (intervention_id, frequency, positive_strategies[0], circumstance[0],
             max_frequency[0], procedure[0], how[0], why[0]))

        social_validity = extract.extract_table(
            'Social validity of seclusion',
            'Authorisation for the use of restrictive practices', tables,
            current_table_position)
        current_table_position = social_validity[1]
        authorisation = extract.extract_table(
            'Authorisation for the use of restrictive practices',
            'People involved in the implementation of this PBSP', tables,
            current_table_position)
        current_table_position = authorisation[1]
        last_id = data_get_last_id_by_intervention(mydb, cur, "seclusion_restraint",
                                   intervention_id)[0][0]

        for temp in social_validity[0]:
            data_insert(mydb, cur, "social_validity5",
                        ("how, " + "who, " + "sr_id"),
                        (tuple(temp + [last_id])))
        for temp in authorisation[0]:
            data_insert(mydb, cur, "authorisation5",
                        ("authorisationBody, " + "approvalPeriod, " + "sr_id"),
                        (tuple(temp + [last_id])))
    else:
        stored_types = []
        stored_types = str(stored_types)
        data_insert(
            mydb, cur, "intervention",
            ("user_id, " + "type, " + "ifProposed"),
            (user_id, stored_types, "no"))
#Page 6
    people = extract.extract_paragraph_given_start(
        "People involved in the implementation of this PBSP",
        "How will implementers of this PBSP be trained to implement the proposed interventions?",
        all_content, current_text_position)
    current_text_position = people[1]
    temp = people[0].split("\n")
    list_people = []
    for i in temp:
        if not i.isspace() and not i:
            list_people.append(i)

    time_frame = extract.extract_paragraph_given_start(
        'Timeframe for plan review',
        "How did you assess the acceptability of the interventions proposed in this PBSP?",
        all_content, current_text_position)
    current_text_position = time_frame[1]

    data_insert(mydb, cur, "implementation",
                ("user_id, " + "people, " + "timeframe"),
                (user_id, str(list_people), time_frame[0]))
    how_implementers = extract.extract_table(
        'How will implementers of this PBSP be trained to implement the proposed interventions?',
        'How will implementers of this PBSP communicate with one another to discuss implementation?',
        tables, current_table_position)
    current_text_position = how_implementers[1]

    implementation_plan = None
    try:
        how_implementers_communicate = extract.extract_table(
            'How will implementers of this PBSP communicate with one another to discuss implementation?',
            'Outline the implementation plan', tables, current_table_position)
        current_text_position = how_implementers_communicate[1]

        # Eddie PDF does not contain this part

        implementation_plan = extract.extract_table(
            'Outline the implementation plan',
            'How will PBSP implementation and goal achievement be reviewed and monitored?',
            tables, current_table_position)
        current_text_position = implementation_plan[1]
    except:
        how_implementers_communicate = extract.extract_table(
            'How will implementers of this PBSP communicate with one another to discuss implementation?',
            'How will PBSP implementation and goal achievement be reviewed and monitored?', tables, current_table_position)
        current_text_position = how_implementers_communicate[1]


    how_implementation = extract.extract_table(
        'How will PBSP implementation and goal achievement be reviewed and monitored?',
        'Timeframe for plan review', tables, current_table_position)
    current_text_position = how_implementation[1]

    last_id = data_get_last_id(mydb, cur, "implementation", user_id)[0][0]

    for temp in how_implementers[0]:
        data_insert(mydb, cur, "how_implementer",
                    ("strategy, " + "responsible, " + "i_id"),
                    (tuple(temp + [last_id])))
    for temp in how_implementers_communicate[0]:
        data_insert(mydb, cur, "how_communicate",
                    ("strategy, " + "responsible, " + "i_id"),
                    (tuple(temp + [last_id])))
    # ip_id can be typo
    if implementation_plan:
        for temp in implementation_plan[0]:
            data_insert(mydb, cur, "implementation_plan",
                        ("action, " + "responsible, " + "ip_id"),
                        (tuple(temp + [last_id])))
    for temp in how_implementation[0]:
        data_insert(mydb, cur, "how_implementation",
                    ("strategy, " + "responsible, " + "i_id"),
                    (tuple(temp + [last_id])))


#social validity
    acceptability = extract.extract_paragraph_given_start(
        "How did you assess the acceptability of the interventions proposed in this PBSP?",
        "Who did you consult with?", all_content, current_text_position)
    current_text_position = acceptability[1]
    who = all_content[current_text_position +
                      len("Who did you consult with?"):]
    data_insert(mydb, cur, "socialv",
                ("user_id, " + "acceptability, " + "who"),
                (user_id, acceptability[0], who))

    return read_db.getAll(cur,mydb,user_id)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
