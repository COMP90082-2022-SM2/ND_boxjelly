import json
import mysql.connector


def getPage1(cur, db, user_id):
    try:
        sql = "SELECT summary from short_summary " \
              "WHERE id = (SELECT MAX(id) from `short_summary` WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage2(cur, db, user_id):
    try:
        sql = "SELECT * FROM assessment a JOIN persons_consulted p ON a.id=p.assessment_id " \
              "WHERE a.id = (SELECT MAX(id) from assessment WHERE user_id = {})".format(user_id)

        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage3(cur, db, user_id):
    try:
        sql = "SELECT * FROM ba_function ba JOIN stc s ON ba.id=s.f_id " \
              "WHERE ba.id = (SELECT MAX(id) from ba_function WHERE user_id = {})".format(user_id)

        cur.execute(sql)

        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getPage4(cur, db, user_id):
    try:
        sql = "SELECT * FROM goal g " \
              "INNER JOIN strategies s ON g.user_id=s.user_id " \
              "AND s.id = (SELECT MAX(id) FROM strategies WHERE user_id = {}) " \
              "INNER JOIN reinforcement r on g.user_id=r.user_id " \
              "AND r.id = (SELECT MAX(id) FROM reinforcement WHERE user_id = {}) " \
              "INNER JOIN de_escalation d on g.user_id=d.user_id " \
              "AND d.id = (SELECT MAX(id) FROM de_escalation WHERE user_id = {}) " \
              "WHERE g.id = (SELECT MAX(id) FROM goal WHERE user_id = {})".format(user_id, user_id, user_id, user_id)

        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


# Page 5 lacks some information at beginning
def getPage5(cur, db, user_id):
    try:
        iv_id = getInterventionId(cur, db, user_id)
        return {"chemicalRestraint": getChemicalRestraint(cur, db, iv_id),
                "physicalRestraint": getPhysicalRestraint(cur, db, iv_id),
                "mechanicalRestraint": getMechanicalRestraint(cur, db, iv_id),
                "environmentalRestraint": getEnvironmentalRestraint(cur, db, iv_id),
                "seclusionRestraint": getSeclusionRestraint(cur, db, iv_id)}
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
            "page5": getPage5(cur, db, user_id)
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
              "JOIN medication m ON c.id=m.cr_id " \
              "JOIN social_validity1 s on c.id=s.cr_id " \
              "JOIN authorisation1 a on c.id=a.cr_id " \
              "WHERE c.iv_id = {}".format(iv_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getPhysicalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM physical_restraint p " \
              "JOIN social_validity2 s on p.id=s.pr_id " \
              "JOIN authorisation2 a on p.id=a.pr_id " \
              "WHERE p.iv_id = {}".format(iv_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getMechanicalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM mechanical_restraint m " \
              "JOIN social_validity3 s on m.id=s.mr_id " \
              "JOIN authorisation3 a on m.id=a.mr_id " \
              "WHERE m.iv_id = {}".format(iv_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getEnvironmentalRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM environmental_restraint e " \
              "JOIN social_validity4 s on e.id=s.er_id " \
              "JOIN authorisation4 a on e.id=a.er_id " \
              "WHERE e.iv_id = {}".format(iv_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getSeclusionRestraint(cur, db, iv_id):
    try:
        sql = "SELECT * FROM seclusion_restraint sr " \
              "JOIN social_validity5 s on sr.id=s.sr_id " \
              "JOIN authorisation5 a on sr.id=a.sr_id " \
              "WHERE sr.iv_id = {}".format(iv_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
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
              "JOIN how_implementer hi1 on i.id=hi1.i_id " \
              "JOIN implementation_plan ip on i.id=ip.ip_id " \
              "JOIN how_communicate hc on i.id=hc.i_id " \
              "JOIN how_implementation hi2 on i.id=hi2.i_id " \
              "WHERE i.id = (SELECT MAX(id) from implementation WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None


def getSocialValidity(cur, db, user_id):
    try:
        sql = "SELECT * FROM socialV " \
              "WHERE id = (SELECT MAX(id) FROM socialV WHERE user_id = {})".format(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except mysql.connector.Error as e:
        print(e)
        return None
