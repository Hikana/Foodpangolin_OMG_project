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



# get
def get_store_list() :
    sql = "SELECT * FROM `store`"
    cursor.execute(sql)
    return cursor.fetchall()

def get_store_menu(sid) :
    sql = "SELECT name, price, intro FROM `store_menu` where sid = %s"
    param = [sid]
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_customer_id(id) :
    # print('============')
    print(id)
    sql = "SELECT id FROM `customer` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_customer_order(order_menu_id) :
    sql = "select id from `store_menu` where id = %s"
    param = (order_menu_id)
    cursor.execute(sql, param)
    return cursor.fetchall()


def get_available_order() :
    sql = "SELECT * FROM `customer_order` WHERE `status` = %s"
    param = [1] # 1 : 待運送, 2: 運送中, 3: 已送達 (可再調整代碼)
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_menu_order():
    sql = "select "




# add
def add_customer_order(id, store_id, destination) :
    sql = """
    INSERT INTO
      `customer_order`
      (`customer_id`, `store_id`, `delivery_id`, `destination`) 
      VALUES ( %s,%s,%s, %s)"""
    param = (id,store_id,str(-1),destination)
    print(param)
    cursor.execute(sql,param)
    # customer_id = cursor.lastrowid
    conn.commit()
    # print(id,store_id,-1,destination)
    sql = "SELECT id FROM `customer_order` WHERE `customer_id` = %s AND `store_id` = %s AND `delivery_id` = %s AND `destination` = %s"
    param = [id,store_id,-1,destination] 
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def add_order_menu(menu_id, customer_order_id) :
    sql = """
    INSERT INTO
      `order_menu`
      (`menu_id`, `customer_order_id`) 
      VALUES ( %s,%s)"""
    param = (menu_id, customer_order_id)
    cursor.execute(sql,param)
    conn.commit()
    return 

def add_store_menu(store_id):
    sql = """
    insert `store_menu` 
    SET
    `name` = %s ,`price` = %s,`intro` = %s ,`status`= %s
    WHERE `sid` = %s
"""
    param = (store_id)
    cursor.execute(sql,param)
    conn.commit()
    return


# edit

def edit_store_menu(store_id):
    sql = """
    UPDATE `store_menu` 
    SET
    `name` = %s ,`price` = %s,`intro` = %s ,`status`= %s
    WHERE `sid` = %s
"""
    param = (store_id)
    cursor.execute(sql,param)
    conn.commit()
    return


