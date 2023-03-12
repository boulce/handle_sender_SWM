import pymysql
import threading

con = pymysql.connect(host='', user='', password='',
                       db='', charset='',                      # 해킹 위험이 있어 비공개로 처리
                       cursorclass=pymysql.cursors.DictCursor) # 한글처리 (charset = 'utf8')
cur = con.cursor()

def init_competition_name_fetch():
    sql = "SELECT name FROM competition_info"
    cur.execute(sql)
    name = cur.fetchone()["name"]
    return name

def init_fetch():
    sql = "SELECT * FROM participant ORDER BY team, sid"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def apply_competition_name(old, new):
    sql = "UPDATE competition_info SET name = %s WHERE name = %s"
    cur.execute(sql, (new, old))
    con.commit()

def add_sql(input_dic):
    #(team, sid, name, email, attendance, handle_id, handle_pw)
    sql = "INSERT INTO participant VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (input_dic['team'], input_dic['sid'], input_dic['name'], input_dic['email']
    , input_dic['attendance'], input_dic['handle_id'], input_dic['handle_pw']))
    con.commit()

def delete_sql(input_dic):
    sql = "DELETE FROM participant WHERE sid = %s"
    cur.execute(sql, (input_dic['sid']))
    con.commit()

def attend_sql(input_dic):
    sql = "UPDATE participant SET attendance = %s WHERE sid = %s"
    cur.execute(sql, ("O", input_dic['sid']))
    con.commit()