import MySQLdb
import json

def getPage1(cur,db,user_id):
    try:
        sql = "SELECT summary FROM short_summary s JOIN users u ON s.user_id=u.id WHERE u.id =" + str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None

def getPage2(cur,db,user_id):
    try:
        sql="SELECT * FROM assessment a JOIN persons_consulted p ON a.id=p.assessment_id WHERE a.user_id = "+ str(user_id)

        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None

def getPage3(cur,db,user_id):
    try:
        sql="SELECT * FROM ba_function ba JOIN stc s ON ba.id=s.f_id WHERE ba.user_id = "+str(user_id)

        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None

def getPage4(cur,db,user_id):
    try:
        sql="SELECT * FROM goal g\
                JOIN strategies s ON g.user_id=s.user_id \
                JOIN reinforcement r on g.user_id=r.user_id \
                JOIN de_escalation d on g.user_id=d.user_id\
                WHERE g.user_id = "+str(user_id)

        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None

# Page 5 lacks some information at beginning
def getPage5(cur,db,user_id):
    try:

        return {"chemicalRestraint":getChemicalRestraint(cur,db,user_id),
                "physicalRestraint":getPhysicalRestraint(cur,db,user_id),
                "mechanicalRestraint":getMechanicalRestraint(cur,db,user_id),
                "environmentalRestraint":getEnvironmentalRestraint(cur,db,user_id),
                "seclusionRestraint":getSeclusionRestraint(cur,db,user_id)}
    except (MySQLdb.Error,MySQLdb.Warning) as e:
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

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getChemicalRestraint(cur,db,user_id):
    try:
        sql = "SELECT * FROM chemical_restraint c\
                JOIN medication m ON c.id=m.cr_id\
                JOIN social_validity1 s on c.id=s.cr_id\
                JOIN authorisation1 a on c.id=a.cr_id\
                WHERE c.user_id = "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getPhysicalRestraint(cur,db,user_id):
    try:
        sql = "SELECT * FROM physical_restraint p \
                JOIN social_validity2 s on p.id=s.pr_id\
                JOIN authorisation2 a on p.id=a.pr_id\
                WHERE p.user_id = "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getMechanicalRestraint(cur,db,user_id):
    try:
        sql = "SELECT * FROM mechanical_restraint m \
                JOIN social_validity3 s on m.id=s.mr_id\
                JOIN authorisation3 a on m.id=a.mr_id\
                WHERE m.user_id = "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getEnvironmentalRestraint(cur,db,user_id):
    try:
        sql = "SELECT * FROM environmental_restraint e\
                JOIN social_validity4 s on e.id=s.er_id\
                JOIN authorisation4 a on e.id=a.er_id\
                WHERE e.user_id = "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getSeclusionRestraint(cur,db,user_id):
    try:
        sql = "SELECT * FROM seclusion_restraint sr\
                JOIN social_validity5 s on sr.id=s.sr_id\
                JOIN authorisation5 a on sr.id=a.sr_id\
                WHERE sr.user_id ="+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None


def getPage6(cur,db,user_id):
    try:

        return {"Implementation":getImplementation(cur,db,user_id),
                "SocialValidity":getSocialValidity(cur,db,user_id)
                }
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None

def getImplementation(cur,db,user_id):
    try:
        sql = "SELECT * FROM implementation i\
                JOIN how_implementer hi1 on i.id=hi1.ii_id\
                JOIN implementation_plan ip on i.id=ip.ii_id\
                JOIN how_communicate hc on i.id=hc.ii_id\
                JOIN how_implementation hi2 on i.id=hi2.ii_id\
                WHERE i.user_id "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def getSocialValidity(cur,db,user_id):
    try:
        sql="SELECT * FROM socialv\
                WHERE g.user_id = "+str(user_id)
        cur.execute(sql)
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
    except (MySQLdb.Error,MySQLdb.Warning) as e:
        print(e)
        return None


