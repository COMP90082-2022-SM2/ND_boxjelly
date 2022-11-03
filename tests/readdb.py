import json
import mysql.connector
import pandas as pd
import collections
def get_json_format(cur):
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

def getPage1(cur, db, user_id):
    try:
        sql = "SELECT summary from short_summary " \
              "WHERE id = (SELECT MAX(id) from `short_summary` WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        paragraph = get_json_format(cur)
        page1 = dict(json.loads(paragraph)[0])
        return page1
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage2(cur, db, user_id):
    try:
        sql = "SELECT * FROM assessment a  " \
              "WHERE a.id = (SELECT MAX(id) from assessment WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        paragraph = get_json_format(cur)

        sql = "SELECT * FROM persons_consulted p " \
              "WHERE p.assessment_id = (SELECT MAX(id) from assessment WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        table = get_json_format(cur)

        paragraph = json.loads(paragraph)

        page2 = dict(paragraph[0])

        page2["persons_consulted"] = table

        return page2


    except mysql.connector.Error as e:
        print(e)
        return None