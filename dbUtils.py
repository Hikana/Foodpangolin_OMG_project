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




# 刪除

def dele_food(id):   # 刪除店家菜單(店家用)
    sql = """
        DELETE FROM `store_menu` 
        WHERE id = %s;
    """
    param = (id,)
    cursor.execute(sql,param)
    conn.commit()
    return



def fix_food(name, price, intro, food_id):
    sql = """
        update `store_menu` 
        SET name=%s, intro=%s ,price=%s
        where id = %s
    """
    param = [name, intro, price, food_id]
    cursor.execute(sql,param)
    conn.commit()
    return

def add_food(name, price, intro, sid):
    sql = """
        insert `store_menu` 
        SET `name`=%s, `intro`=%s ,`price`=%s, `sid`=%s
    """
    param = (name, price, intro, sid)
    cursor.execute(sql,param)
    conn.commit()
    return



def the_food(id) : # 自己的菜單
    sql = """
        SELECT *
        FROM `store_menu` 
        WHERE id = %s
    """
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchone()

def store_own_list(id) : # 店家自己的菜單
    sql = """
        SELECT *
        FROM `store_menu` 
        WHERE sid = %s
    """
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()



# def get_store_self_order_list(store_id) :
#     sql = "SELECT * FROM `customer_order` where status = 1 and store_id = %s"
#     param = [store_id]
#     cursor.execute(sql,param)
#     return cursor.fetchall()

# def get_store_self_order_list(id) : # 三張表組合
#     sql = """
#         SELECT *
#         FROM `customer_order` 
#         inner join `order_menu` on customer_order.id = order_menu.customer_order_id
#         inner join `store_menu` on store_menu.id = order_menu.menu_id
#         WHERE customer_order.status = 1 and store_id= %s
#     """
#     param = [id]
#     cursor.execute(sql,param)
#     return cursor.fetchall()

def meal_status_complete(id) :
    sql = """
        UPDATE `customer_order` 
        set status = 2
        WHERE id = %s
    """
    param = [id]
    cursor.execute(sql, param)
    conn.commit()
    return    




def get_all_users() : # get infom from user 
    sql = "SELECT * FROM `user`"
    cursor.execute(sql,)
    return cursor.fetchall()

def get_price(id) : # "新" 三張表組合 ， 為了 order_id
    sql = """
        SELECT price
        FROM `customer_order` 
        inner join `order_menu` on customer_order.id = order_menu.customer_order_id
        inner join `store_menu` on store_menu.id = order_menu.menu_id
        WHERE customer_order_id = %s
    """
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchone()




def edit_sumry(cid,sid,did,price) : 
    sql = """
        UPDATE `user` 
        inner join store on user.id = store.uid
        set `summary` = summary+%s 
        WHERE store.id = %s
    """
    param = (int(price),sid,)
    cursor.execute(sql, param)
    conn.commit()

    sql = """
        UPDATE `user` 
        inner join customer on user.id = customer.uid
        set `summary` = summary+%s 
        WHERE customer.id = %s
    """
    param = (int(price),cid)
    cursor.execute(sql, param)
    conn.commit()

    sql = """
        UPDATE `user` 
        inner join delivery on user.id = delivery.uid
        set `summary` = `summary` + 1 
        WHERE delivery.id = %s
    """
    param = (did,)
    
    print("+++++++++++++",param)
    cursor.execute(sql, param)
    conn.commit()
    return
    



# get

# 顧客用

def get_customer_id(id) : # 顧客的 ID ，點餐用 ##
    sql = "SELECT id FROM `customer` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_store_list() : # 商店清單(給顧客) ##
    sql = "SELECT id, name, intro, location FROM `store`"
    cursor.execute(sql)
    return cursor.fetchall()

def get_store_menu(sid) : # 商店的菜單 ##
    sql = "SELECT id, name, intro, price FROM `store_menu` where sid = %s"
    param = [sid]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_customer_self_order(customer_id) : # 顧客自己的訂單 ##
    sql = """
        select customer_order.time, store.name as s_name, store_menu.name as m_name, customer_order.quantity, delivery.name as d_name, customer_order.quantity*store_menu.price as total, customer_order.status
        from `customer_order`
        INNER JOIN 
        `store` ON store.id = customer_order.store_id
        LEFT JOIN
        `delivery` ON delivery.id = customer_order.delivery_id
        INNER JOIN
        `order_menu` ON order_menu.customer_order_id = customer_order.id
        INNER JOIN
        `store_menu` ON store_menu.id = order_menu.menu_id
        WHERE customer_order.customer_id = %s
        """
    param = [customer_id]
    print("=======================",param)
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_menu(id) : # 看菜單詳細 ##
    sql = "select sid, name, price, intro from `store_menu` where id = %s"
    param = [id]
    cursor.execute(sql, param)
    return cursor.fetchall()




# 送貨員
def get_delivery_id(id) : # 送貨員 ID ，接單用 ##
    sql = "SELECT id FROM `delivery` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_available_order() : # 找到還沒被接的訂單，送貨員首頁用 ##
    sql = """
        SELECT customer_order.status, customer_order.id, store_menu.name as order_name, store.name as store, customer_order.quantity, store_menu.price, customer_order.destination, customer_order.quantity*store_menu.price as total 
        FROM order_menu
        inner join customer_order on order_menu.customer_order_id = customer_order.id
        inner join store_menu on order_menu.menu_id = store_menu.id
        inner join store on store_menu.sid = store.id
        WHERE customer_order.status = %s
    """
    param = [1] # 1: 待運送, 2: 運送中, 3: 已送達 (可再調整代碼)
    cursor.execute(sql,param)
    
    return cursor.fetchall()

# def get_available_order() : # 找到還沒被接的訂單，送貨員首頁用 ##
#     sql = """
#         SELECT customer_order.status, customer_order.id, store_menu.name as order_name, store.name as store, customer_order.quantity, store_menu.price, customer_order.destination, customer_order.quantity*store_menu.price as total 
#         FROM order_menu
#         inner join customer_order on order_menu.customer_order_id = customer_order.id
#         inner join store_menu on order_menu.menu_id = store_menu.id
#         inner join store on store_menu.sid = store.id
#         WHERE customer_order.status = %s
#     """
#     param = [1] # 1: 待運送, 2: 運送中, 3: 已送達 (可再調整代碼)
#     cursor.execute(sql,param)
    
#     return cursor.fetchall()

# def get_customer_order(order_menu_id) : # 待送訂單的詳細，送貨員接單用
#     sql = """
#         SELECT customer_order.status, customer_order.id, store_menu.name as order_name, store.name as store, customer_order.quantity, store_menu.price, customer_order.destination, customer_order.quantity*store_menu.price as total 
#         FROM order_menu
#         inner join customer_order on order_menu.customer_order_id = customer_order.id
#         inner join store_menu on order_menu.menu_id = store_menu.id
#         inner join store on store_menu.sid = store.id
#         WHERE customer_order.id = %s
#     """
#     param = [order_menu_id]
#     print(param)
#     cursor.execute(sql, param)
#     return cursor.fetchall()

def get_store_id(id) : # 商店 ID ，新增菜單用 ##
    sql = "SELECT id FROM `store` where uid = %s"
    param = [id]
    cursor.execute(sql,param)
    return cursor.fetchall()

def get_order(sid): # 列出店家的訂單
    sql = """
        SELECT customer.name, delivery.name, store_menu.name, customer_order.destination 
        FROM `customer_order`
        INNER JOIN `customer` ON customer_order.customer_id = customer.id
        INNER JOIN `delivery` ON customer_order.delivery_id = delivery.id
        INNER JOIN `order_menu` ON order_menu.customer_order_id = customer_order.id
        INNER JOIN `store_menu` ON store_menu.id = order_menu.menu_id
        INNER JOIN `store` ON customer_order.store_id = store.id
        WHERE store.id = %s"""
    param = [sid]
    print(param)
    cursor.execute(sql, param)
    return cursor.fetchall()

# def get_customer_all_order(order_menu_id) : # 拿到所有用戶的 ID
#     sql =  "SELECT customer_id, store_id, delivery_id FROM customer_order where id = %s"
#     cursor.execute(sql, (order_menu_id,))
#     return cursor.fetchall()



def get_menu_order(order): # 找到餐點的 ID，點餐用（要加進 order_menu）
    sql = "SELECT `id` FROM `store_menu` WHERE name = %s"
    param = [order]
    cursor.execute(sql, param)
    return cursor.fetchone()

def get_delivery_order_list(delivery_id): # 找到外送員已接的訂單（目的地、客戶姓名、商店、餐點內容） ##
    sql = """
        SELECT customer.name, customer_order.status, customer_order.id, store_menu.name as order_name, store.name as store, customer_order.quantity, store_menu.price, customer_order.destination, customer_order.quantity*store_menu.price as total 
        FROM order_menu
        inner join customer_order on order_menu.customer_order_id = customer_order.id
        inner join store_menu on order_menu.menu_id = store_menu.id
        inner join store on store_menu.sid = store.id
        inner join customer on customer.id = customer_order.customer_id
        WHERE customer_order.delivery_id = %s and customer_order.status = 2
        """
    param = [delivery_id]
    cursor.execute(sql, param)
    return cursor.fetchall()




# add

# 顧客
def add_customer_order(id, store_id, quantity, destination) : # 顧客點餐 ##
    sql = """
    INSERT INTO
      `customer_order`
      (`customer_id`, `store_id`, `quantity`, `delivery_id`, `destination`,`status`) 
      VALUES ( %s,%s,%s,%s,%s,%s)"""
    param = [id,store_id,quantity,str(-1),destination,str(1)]
    print(param)
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

def edit_customer_delivery(delivery_id, status, order_menu_id) : # 接單後把 delivery_id 的 -1 改成送貨員的 ID / 加上 status 更改
    sql = """
        UPDATE `customer_order` 
        inner join `order_menu` on order_menu.customer_order_id = customer_order.id
        set customer_order.delivery_id = %s,customer_order.status = %s
        WHERE order_menu.customer_order_id = %s
    """
    param = (delivery_id,status,order_menu_id)
    cursor.execute(sql, param)
    conn.commit()
    return



