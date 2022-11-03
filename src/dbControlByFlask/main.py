# http://localhost/phpmyadmin/
from flask import Flask, redirect, url_for, render_template, request, session, flash
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from model import Users #, Assessment,ShortSummary, BAfunction, Goal, Strategies, Reinforcement, DeEscalation
from exts import db, app

from pdf_reader import table_extraction, extract_answers, page_info
from data_inserter import data_insert, data_update
from sub_column_data_inserter import sub_column_data_insert, ref_table

import pandas as pd 
import mysql.connector 
import logging  
import sys

from sqlalchemy import create_engine, inspect

from read_from_db import getPage1

# includes all the table names on each page of the PDF and all the attributes for each table. 
table_dict = {1: [("short_summary", "user_id, summary")], 
    3:[("assessment", "user_id, behaviouralAssessment, nonBehaviouralAssessment")], 
    4:[("ba_function", "user_id, functionName"), ("ba_function", "user_id, description, summary, proposedAlternative")], 
        5: [("goal", "user_id, behaviour, life"), ("strategies", "user_id, environment, teaching, others")], 
    7: [("reinforcement", "user_id, reinforcer, schedule, howIdentified"), ("de_escalation", "user_id, howtoPrompt, strategies, postIncident")], 
    9: [("intervention", "user_id, ifProposed"), ("intervention", "user_id, type"), ("chemical_restraint", "positiveStrategy, circumstance, procedure, howRestrainReduce, why")], 
    10:[("physical_restraint", "intervention_id, description, positiveStrategy, circumstance, procedure, how, why"), ("mechanical_restraint", "description, positiveStrategy, circumstance, procedure, howKnow, howRestraint, why")], 
    11:[("environmental_restraint", "description, frequency, positive_strategy, circumstance, person, procedure, impact, howImpact, howRestraint, why")], 
    12:[("seclusion_restraint", "frequency, positiveStrategy, circumstance, maxFrequency, procedure, how, why")], 
    13:[("implementation", "user_id, people, timeframe")], 14:[("socialv", "user_id, acceptability, who")]
    } 
 
sub_column_table_info = {3: ["persons_consulted"], 4: ["STC"], 9: ["medication", "social_validity1", "authorisation1"], 
                        10: ["social_validity2", "authorisation2", "social_validity3", "authorisation3"], 
                        11: ["social_validity4", "authorisation4"], 12: ["social_validity5", "authorisation5"], 
                        13: ["how_implementer", "implementation_plan", "how_communicate", "how_implementation"], 
                        14: ["socialv"]}
 
mydb = mysql.connector.connect( 
        user = 'bcad2e6d9226f9', 
        host = 'us-cdbr-east-06.cleardb.net', 
        password = '318b6978', 
        database = 'heroku_f7c500f08d32a48',
        connect_timeout=1000
     )
cur = mydb.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["GET", "POST"])
def process_pdf():
    engine = create_engine('mysql://bcad2e6d9226f9:318b6978@us-cdbr-east-06.cleardb.net/heroku_f7c500f08d32a48')
    inspector=inspect(engine) 
    print(inspector.has_table('user'))  
    if inspector.has_table('user') == False: # if tables haven't created yet, create all tables based on db.model
        db.create_all()

    data_insert(mydb, cur, "users", "name", ("user1", ))  
    
    user = Users.query.filter(Users.name == "user1").first() # get user id for other tables' user id foreign key
    for page_num in [1,3,4,5,7,9,13,14]:
        continuous = page_info[page_num]['continuous']
        next_page = page_info[page_num]['next_page']
        sub_col_answers = [] 
        sub_col_answers_all = [] 
        table_lists = table_extraction(page_num)
        if page_num-1 in page_info and page_info[page_num-1]["next_page"] == True : #ignore the table that continutes from the previous page
            if len(table_lists) > 1:
                answers_all,sub_col_answers_all = extract_answers(table_lists[1:])
        else:
            answers_all,sub_col_answers_all = extract_answers(table_lists)
             
        if continuous: # continous next page for the same section/attribute
            next_table_lists = table_extraction(page_num+1)
            next_page_txt = next_table_lists[0][0] #texts from the same section
            answers_all[-1][0] += str(next_page_txt)
            next_table_lists[0].pop(0) # pop the content that continued from the previous page
            
        if next_page or sum(len(string[1].split(",")) for string in table_dict[page_num]) - len(table_dict[page_num]) > sum(len(i) for i in answers_all):
            
            if not continuous:
                next_table_lists = table_extraction(page_num+1)
            if page_num+1 == 6: # two lines in that question - concatenate to one
                
                next_table_lists[0][0][0] = next_table_lists[0][0][0] + next_table_lists[0][1][0]
                next_table_lists[0].pop(1)
            next_answers,sub_col_answers = extract_answers(next_table_lists)
            
            next_page = True
    
        table_index = 0
        for db_table, attribute in table_dict[page_num]:
            attr_index = 1
            if db_table not in ref_table: #i.e. chemical_restraint: has no user_id
                value = (user.id,)
            else:
                ref_table_name = ref_table[db_table]
                fk_name = ref_table_name.lower() + "_id"
                sql = "SELECT MIN(id) FROM " + ref_table_name
                cur.execute(sql)
                f_k_id = int(cur.fetchall()[0][0])
                value = (f_k_id, )
                
            while attr_index < len(answers_all[table_index])+1:
                v = str(answers_all[table_index][attr_index-1]).replace('\r', ' ').replace(r'\r', ' ')
                if v[0] == "[":
                    v = v[2:-2]
                value += (v,) 
                attr_index += 1

            next_attr_index = 0 
            while next_page and table_index > 0 and next_attr_index < len(next_answers[0]) and attr_index < len(attribute.split())+1:
                v = str(next_answers[0][next_attr_index]).replace('\r', ' ').replace(r'\r', ' ')
                if v[0] == '[':
                    v = v[2:-2]
                value += (v, ) 
                next_attr_index += 1
            table_index += 1
            
            if db_table in ref_table:
                print("Trueeeeeeee")
                ref_table_name = ref_table[db_table]
                fk_name = ref_table_name.lower() + "_id"
                sql = "SELECT MIN(id) FROM " + ref_table_name
                cur.execute(sql)
                f_k_id = int(cur.fetchall()[0][0])
                
                fk_val = (f_k_id, ) 
                fk_val += value
                
                try:
                    data_insert(mydb, cur, db_table, attribute, fk_val)
                except:
                    pass # contains no answers, doesn't need to extract
                
            else:                 
                sql = "SELECT * FROM " + db_table               
                cur.execute(sql) 
                if cur.fetchall():                  
                    data_update(mydb, cur, db_table, attribute, value[:len(attribute.split())])
                else:           
                    data_insert(mydb, cur, db_table, attribute, value[:len(attribute.split())])
                

        if sub_col_answers_all: # meaning there's a sub table in that page 
            if next_page:
                next_sub_table_lists = table_extraction(page_num+1)
                next_answers2, next_sub_answers = extract_answers(next_sub_table_lists)
            
            for i in range(len(sub_column_table_info[page_num]) - len(sub_col_answers_all)): # how many sub-col tables in the next page
                sub_col_answers_all.append(next_sub_answers[i]) #append next page's sub-col table texts to all sub-col=answers
            
            sub_column_data_insert(mydb, cur, page_num, sub_column_table_info, sub_col_answers_all)               
    #dict1 = getPage1(cur, mydb, 4)
    cur.close()
    db.session.close()
    #return dict1
    return "successful"
    # for testing/reading from database requirement
    #return redirect(url_for("view"))

@app.route("/view")
def view():
    dict1 = getPage1(cur, mydb, 4)
    cur.close()
    db.session.close()
    return dict1
#     # https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
#     # https://stackoverflow.com/questions/18150144/how-to-query-a-database-after-render-template
#     # cur.execute("SELECT * FROM short_summary")
#     # data = cur.fetchall()
#     # return render_template("view.html", data=data)
#     users_table = Users.query.all()
#     short_summary_table = Shortsummary.query.all()
#     assessment_table = Assessment.query.all()
#     ba_function_table = Bafunction.query.all()
#     goal_table = Goal.query.all()
#     strategies_table = Strategies.query.all()
#     reinforcement_table = Reinforcement.query.all()
#     de_escalation_table = Deescalation.query.all()
#     cur.close()
#     db.session.close()
#     return render_template("view.html", users_table=users_table, short_summary_table=short_summary_table, 
#     assessment_table=assessment_table, ba_function_table=ba_function_table, goal_table=goal_table, 
#     strategies_table=strategies_table, reinforcement_table=reinforcement_table, de_escalation_table=de_escalation_table)
#     # return render_template("view.html", values=users.query.all())  # get all the users and pass as objects to value

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    print(app.logger.addHandler(logging.StreamHandler(sys.stdout)))
    print(app.logger.setLevel(logging.ERROR))


