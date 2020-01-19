from news import db_properties


# 通过用户名判断是否有数据
def get_by_name(name):
    sql = "SELECT * FROM itchat_users WHERE name = '%s'" % name
    try:
        conn = db_properties.conn
        conn.ping()
    except Exception:
        conn = db_properties.conn
    cursor = conn.cursor()
    cursor.execute(query=sql)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row != None:
        return True
    return False


# 获取数据库不发送的用户
def get_users():
    userUserName = []
    try:
        conn = db_properties.conn
        conn.ping()
    except Exception:
        conn = db_properties.conn
    cursor = conn.cursor()
    cursor.execute(query="SELECT * FROM itchat_users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        userUserName.append(row[0])
    return userUserName


# 添加黑名单用户
def ins_users(name):
    if get_by_name(name):
        print('用户存在')
        return
    sql = "INSERT INTO itchat_users (name) VALUES ('%s')" % name
    print(sql)
    try:
        conn = db_properties.conn
        conn.ping()
    except Exception:
        conn = db_properties.conn
    cursor = conn.cursor()
    cursor.execute(query=sql)
    conn.commit()
    cursor.close()
    conn.close()


# 删除用户
def del_users(name):
    if get_by_name(name):
        sql = "DELETE FROM itchat_users WHERE name = '%s'" % name
        print(sql)
        try:
            conn = db_properties.conn
            conn.ping()
        except Exception:
            conn = db_properties.conn
        cursor = conn.cursor()
        cursor.execute(query=sql)
        conn.commit()
        cursor.close()
        conn.close()


# 获取数据库发送的群
def get_groups():
    groupUserName = []
    try:
        conn = db_properties.conn
        conn.ping()
    except Exception:
        conn = db_properties.conn
    cursor = conn.cursor()
    cursor.execute(query="SELECT * FROM itchat_groups")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        groupUserName.append(row[0])
    return groupUserName
