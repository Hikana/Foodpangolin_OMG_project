#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
    #連線DB
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="food"
    )
    #建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
    cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)


#登入

def login(username, password):
    """驗證用戶的帳號和密碼，返回用戶資訊或 None。"""
    sql = "SELECT * FROM `user` WHERE username = %s AND password = %s"
    param=(username, password)
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_store_list() :
    sql = "SELECT * FROM `store`"
    cursor.execute(sql)
    return cursor.fetchall()

def get_store_menu(sid) :
    sql = "SELECT name FROM `store_menu` where sid = %s"
    param = [sid]
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_customer_id(id) :
    print('============')
    print(id)
    sql = "SELECT id FROM `customer` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def add_customer_order(id, store_id) :
    sql = """
    INSERT INTO
      `customer_order`
      (`customer_id`, `store_id`, `delivery_id`) 
      VALUES ( %s,%s,%s)"""
    param = (id,store_id,-1)
    cursor.execute(sql,param)
    conn.commit()
    return 



