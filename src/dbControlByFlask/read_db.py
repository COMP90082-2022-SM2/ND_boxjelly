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


def getPage3(cur, db, user_id):
    try:
        sql = "SELECT * FROM ba_function ba "\
              "WHERE ba.id = (SELECT MAX(id) from ba_function WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        paragraph = get_json_format(cur)


        sql = "SELECT * FROM stc s " \
              "WHERE s.f_id = (SELECT MAX(id) from ba_function WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        table = get_json_format(cur)
        paragraph = json.loads(paragraph)
        page3 = dict(paragraph[0])
        page3["stc"] = table
        return page3
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage4(cur, db, user_id):
    try:
        sql = "SELECT * FROM goal g " \
              "WHERE g.id = (SELECT MAX(id) FROM goal WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        goal = get_json_format(cur)
        goal = json.loads(goal)[0]

        sql = "SELECT * FROM strategies s " \
              "WHERE s.id = (SELECT MAX(id) FROM strategies WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        strategies = get_json_format(cur)

        sql = "SELECT * FROM reinforcement r " \
              "WHERE r.id = (SELECT MAX(id) FROM reinforcement WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        reinforcement = get_json_format(cur)

        sql = "SELECT * FROM de_escalation d " \
              "WHERE d.id = (SELECT MAX(id) FROM de_escalation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        de_escalation = get_json_format(cur)

        page4 = {
            "goal":goal,
            "strategies":strategies,
            "reinforcement":reinforcement,
            "de_eslation":de_escalation
        }

        return page4
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage5(cur, db, user_id):
    try:
        sql = "SELECT * FROM intervention i " \
              "WHERE i.id = (SELECT MAX(id) FROM intervention WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        intervention = get_json_format(cur)
        intervention = json.loads(intervention)[0]

        iv_id = getInterventionId(cur, db, user_id)
        page5 = {"intervention":intervention,
                 "chemicalRestraint": None,
                 "physicalRestraint": None,
                 "mechanicalRestraint": None,
                 "environmentalRestraint": None,
                 "seclusionRestraint": None
                 }
        print(intervention)
        if intervention['ifProposed']=='yes':
            types = intervention['type'].strip("[]").replace('\'','').replace(',','').split()
            print(types)
            if 'Chemical' in types:
                page5["chemicalRestraint"] = getChemicalRestraint(cur, db, iv_id)
            if 'Physical' in types:
                page5["physicalRestraint"] = getPhysicalRestraint(cur, db, iv_id)
            if 'Mechanical' in types:
                page5["mechanicalRestraint"] = getMechanicalRestraint(cur, db, iv_id)
            if 'Environmental' in types:
                page5["environmentalRestraint"] = getEnvironmentalRestraint(cur, db, iv_id)
            if 'Seclusion' in types:
                page5["seclusionRestraint"] = getSeclusionRestraint(cur, db, iv_id)

        return page5

    except mysql.connector.Error as e:
        print(e)
        return None


def getAll(cur, db, user_id):
    try:
        return {
            "page1": getPage1(cur, db, user_id),
            "page2": getPage2(cur, db, user_id),
            "page3": getPage3(cur, db, user_id),
            "page4": getPage4(cur, db, user_id),
            "page5": getPage5(cur, db, user_id),
            "page6": getPage6(cur, db, user_id)
        }

    except mysql.connector.Error as e:
        print(e)
        return None


def getInterventionId(cur, db, user_id):
    try:
        sql = "SELECT MAX(id) FROM intervention i " \
              "WHERE i.user_id = {}".format(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        iv_id = cur.fetchall()
        return int(iv_id[0][0])
    except mysql.connector.Error as e:
        print(e)
        return None


def getChemicalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM chemical_restraint c " \
              "WHERE c.iv_id = {}".format(iv_id)
        cur.execute(sql)
        chemical_restraint = get_json_format(cur)
        print(chemical_restraint)
        chemical_restraint = json.loads(chemical_restraint)[0]

        sql = "SELECT * FROM medication m " \
              "WHERE m.cr_id = (SELECT MAX(id) FROM chemical_restraint c WHERE c.iv_id = {})".format(iv_id)
        cur.execute(sql)
        medication = get_json_format(cur)

        sql = "SELECT * FROM social_validity1 s " \
              "WHERE s.cr_id = (SELECT MAX(id) FROM chemical_restraint c WHERE c.iv_id = {})".format(iv_id)
        cur.execute(sql)
        social_validity1 = get_json_format(cur)

        sql = "SELECT * FROM authorisation1 a " \
              "WHERE a.cr_id = (SELECT MAX(id) FROM chemical_restraint c WHERE c.iv_id = {})".format(iv_id)
        cur.execute(sql)
        authorisation1 = get_json_format(cur)

        chemical_restraint["medication"] = medication
        chemical_restraint["social_validity1"] = social_validity1
        chemical_restraint["authorisation1"] = authorisation1

        return chemical_restraint
    except mysql.connector.Error as e:
        print(e)
        return None


def getPhysicalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM physical_restraint p " \
              "WHERE p.iv_id = {}".format(iv_id)
        cur.execute(sql)
        physical_restraint = get_json_format(cur)
        physical_restraint = json.loads(physical_restraint)[0]

        sql = "SELECT * FROM social_validity2 s " \
              "WHERE s.pr_id = (SELECT MAX(id) FROM physical_restraint p WHERE p.iv_id = {})".format(iv_id)
        cur.execute(sql)
        social_validity = get_json_format(cur)

        sql = "SELECT * FROM authorisation2 a " \
              "WHERE a.pr_id = (SELECT MAX(id) FROM physical_restraint p WHERE p.iv_id = {})".format(iv_id)
        cur.execute(sql)
        authorisation = get_json_format(cur)

        physical_restraint["social_validity1"] = social_validity
        physical_restraint["authorisation1"] = authorisation

        return physical_restraint


    except mysql.connector.Error as e:
        print(e)
        return None


def getMechanicalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM mechanical_restraint m " \
              "WHERE m.iv_id = {}".format(iv_id)
        cur.execute(sql)
        mechanical_restraint = get_json_format(cur)
        mechanical_restraint = json.loads(mechanical_restraint)[0]

        sql = "SELECT * FROM social_validity3 s " \
              "WHERE s.mr_id = (SELECT MAX(id) FROM mechanical_restraint m WHERE m.iv_id = {})".format(iv_id)
        cur.execute(sql)
        social_validity = get_json_format(cur)

        sql = "SELECT * FROM authorisation3 a " \
              "WHERE a.mr_id = (SELECT MAX(id) FROM mechanical_restraint m WHERE m.iv_id = {})".format(iv_id)
        cur.execute(sql)
        authorisation = get_json_format(cur)

        mechanical_restraint["social_validity3"] = social_validity
        mechanical_restraint["authorisation3"] = authorisation

        return mechanical_restraint


    except mysql.connector.Error as e:
        print(e)
        return None


def getEnvironmentalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM environmental_restraint e " \
              "WHERE e.iv_id = {}".format(iv_id)
        cur.execute(sql)
        environmental_restraint = get_json_format(cur)
        environmental_restraint = json.loads(environmental_restraint)[0]

        sql = "SELECT * FROM social_validity4 s " \
              "WHERE s.er_id = (SELECT MAX(id) FROM environmental_restraint e WHERE e.iv_id = {})".format(iv_id)
        cur.execute(sql)
        social_validity = get_json_format(cur)

        sql = "SELECT * FROM authorisation4 a " \
              "WHERE a.er_id = (SELECT MAX(id) FROM environmental_restraint e WHERE e.iv_id = {})".format(iv_id)
        cur.execute(sql)
        authorisation = get_json_format(cur)

        environmental_restraint["social_validity4"] = social_validity
        environmental_restraint["authorisation4"] = authorisation

        return environmental_restraint


    except mysql.connector.Error as e:
        print(e)
        return None


def getSeclusionRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM seclusion_restraint sr " \
              "WHERE sr.iv_id = {}".format(iv_id)
        cur.execute(sql)
        seclusion_restraint = get_json_format(cur)
        seclusion_restraint = json.loads(seclusion_restraint)[0]

        sql = "SELECT * FROM social_validity5 s " \
              "WHERE s.sr_id = (SELECT MAX(id) FROM seclusion_restraint sr WHERE sr.iv_id = {})".format(iv_id)
        cur.execute(sql)
        social_validity = get_json_format(cur)

        sql = "SELECT * FROM authorisation5 a " \
              "WHERE a.sr_id = (SELECT MAX(id) FROM seclusion_restraint sr WHERE sr.iv_id = {})".format(iv_id)
        cur.execute(sql)
        authorisation = get_json_format(cur)

        seclusion_restraint["social_validity4"] = social_validity
        seclusion_restraint["authorisation4"] = authorisation

        return seclusion_restraint


    except mysql.connector.Error as e:
        print(e)
        return None


def getPage6(cur, db, user_id):
    try:

        return {"Implementation": getImplementation(cur, db, user_id),
                "SocialValidity": getSocialValidity(cur, db, user_id)
                }
    except mysql.connector.Error as e:
        print(e)
        return None


def getImplementation(cur, db, user_id):
    try:
        sql = "SELECT * FROM implementation i " \
              "WHERE i.id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        implementation = get_json_format(cur)
        implementation = json.loads(implementation)[0]


        sql = "SELECT * FROM how_implementer h " \
              "WHERE h.i_id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        how_implementer = get_json_format(cur)

        sql = "SELECT * FROM implementation_plan ip " \
              "WHERE ip.ip_id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        implementation_plan = get_json_format(cur)

        sql = "SELECT * FROM how_communicate hc " \
              "WHERE hc.i_id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        how_communicate = get_json_format(cur)

        sql = "SELECT * FROM how_implementation hi " \
              "WHERE hi.i_id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        how_implementation = get_json_format(cur)

        implementation['how_implementer'] = how_implementer
        implementation['implementation_plan'] = implementation_plan
        implementation['how_communicate'] = how_communicate
        implementation['how_implementation'] = how_implementation

        return implementation
    except mysql.connector.Error as e:
        print(e)
        return None


def getSocialValidity(cur, db, user_id):
    try:
        sql = "SELECT * FROM socialV " \
              "WHERE id = (SELECT MAX(id) FROM socialV WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        socialV = get_json_format(cur)
        socialV = json.loads(socialV)[0]

        return socialV
    except mysql.connector.Error as e:
        print(e)
        return None
