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
    sql = "SELECT * FROM `user` WHERE username = %s AND password = %s"
    param=(username, password)
    cursor.execute(sql,param)
    return cursor.fetchall()



# get
def get_store_list() : # 商店清單(給顧客)
    sql = "SELECT * FROM `store`"
    cursor.execute(sql)
    return cursor.fetchall()

def get_store_menu(sid) : # 商店的菜單
    sql = "SELECT name, price, intro FROM `store_menu` where sid = %s"
    param = [sid]
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_customer_id(id) : # 顧客的 ID ，點餐用
    sql = "SELECT id FROM `customer` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_delivery_id(id) : # 送貨員 ID ，接單用
    sql = "SELECT id FROM `delivery` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_customer_order(order_menu_id) : # 待送訂單的詳細，送貨員接單用
    sql = """
        SELECT str_m.name as "order", s.name as "store", str_m.price, cus_o.destination 
        FROM `order_menu` as odr_m 
        inner join `customer_order` as cus_o on odr_m.customer_order_id = cus_o.id
        inner join `store_menu` as str_m on odr_m.menu_id = str_m.id
        inner join `store` as s on str_m.sid = s.id
        WHERE odr_m.id = %s
    """
    param = [order_menu_id]
    print(param)
    cursor.execute(sql, param)
    return cursor.fetchall()


def get_available_order() : # 找到還沒被接的訂單，送貨員首頁用
    sql = """
        SELECT str_m.name, s.name, str_m.price, cus_o.destination 
        FROM `order_menu` as odr_m 
        inner join `customer_order` as cus_o on odr_m.customer_order_id = cus_o.id
        inner join `store_menu` as str_m on odr_m.menu_id = str_m.id
        inner join `store` as s on str_m.sid = s.id
        WHERE cus_o.status = %s
    """
    param = [1] # 1 : 待運送, 2: 運送中, 3: 已送達 (可再調整代碼)
    cursor.execute(sql,param)
    
    return cursor.fetchall()

def get_menu_order(order): # 找到餐點的 ID，點餐用（要加進 order_menu）
    sql = "SELECT `id` FROM `store_menu` WHERE name = %s"
    param = [order]
    cursor.execute(sql, param)
    return cursor.fetchone()

def get_delivery_order_list(delivery_id): # 找到外送員已接的訂單（目的地、客戶姓名、商店、餐點內容）
    sql = """
        SELECT customer_order.status customer_order.destination, customer.name, store.name, store_menu.name 
        FROM `customer_order`
        INNER JOIN `customer` ON customer.id = customer_order.customer_id
        INNER JOIN `store` ON store.id = customer_order.store_id
        INNER JOIN `order_menu` ON customer_order.id = order_menu.customer_order_id
        INNER JOIN `store_menu` ON order_menu.menu_id = store_menu.id
        WHERE customer_order.delivery_id = %s
        """
    param = [delivery_id]
    cursor.execute(sql, param)
    return cursor.fetchall()




# add
def add_customer_order(id, store_id, destination) :
    sql = """
    INSERT INTO
      `customer_order`
      (`customer_id`, `store_id`, `delivery_id`, `destination`,`status`) 
      VALUES ( %s,%s,%s,%s,%s)"""
    param = (id,store_id,str(-1),destination,str(1))
    cursor.execute(sql,param)
    conn.commit()
    customer_id = cursor.lastrowid
    
    return customer_id

def add_order_menu(menu_id, customer_order_id) :
    sql = """
    INSERT INTO
      `order_menu`
      (`menu_id`, `customer_order_id`) 
      VALUES (%s,%s)"""
    param = [menu_id, customer_order_id]
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

def edit_customer_delivery(delivery_id,order_menu_id) : # 接單後把 delivery_id 的 -1 改成送貨員的 ID
    sql = """
        UPDATE `customer_order` 
        inner join `order_menu` on order_menu.customer_order_id = customer_order.id
        set customer_order.delivery_id = %s
        WHERE order_menu.id = %s
    """
    param = (delivery_id,order_menu_id)
    print(param)
    cursor.execute(sql, param)
    return


