def data_insert(mydb, cur, db_table, attribute, value):
    if len(attribute.split()) == 1:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s)"
    elif len(attribute.split()) == 2:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s)"
    elif len(attribute.split()) == 3:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s)"
    elif len(attribute.split()) == 4:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s)"
    elif len(attribute.split()) == 5:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s)"
    elif len(attribute.split()) == 6:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s, %s)"
    elif len(attribute.split()) == 7:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
    elif len(attribute.split()) == 8:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    elif len(attribute.split()) == 9:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    elif len(attribute.split()) == 10:
        sql = "INSERT INTO " + db_table + "(" + attribute + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # cur.execute(sql, ("abc",))
    print(sql)
    cur.execute(sql, value)
    mydb.commit()

def data_get_last_id(mydb, cur,db_table,user_id):
    sql ="SELECT MAX(id) FROM "+db_table +" WHERE user_id = "+str(user_id)
    print(sql)
    cur.execute(sql)
    id = cur.fetchall()
    mydb.commit()
    return id