from flask import Flask, render_template, request, session, redirect
from functools import wraps
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
		database="bidplatform"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)


#登入

def login(account, password):
    """驗證用戶的帳號和密碼，返回用戶資訊或 None。"""
    sql = "SELECT * FROM `user` WHERE account = %s AND password = %s"
    param=(account, password)
    cursor.execute(sql,param)
    return cursor.fetchall()


#新增資料

def add_price(pid, bid_price, UID):  # 用戶幫商品加價
	
	sql="INSERT INTO record (pid, BidPrice, UID) VALUES (%s, %s, %s)"
	param=(pid, bid_price, UID)
	cursor.execute(sql,param)
	conn.commit()
	return

def add_product(ProductName, Introduce, StartPrice, UID):  # 新增商品
	sql='''
	insert into 
	product(ProductName, Introduce, StartPrice, UID) 
	values (%s, %s, %s, %s);'''
	param=(ProductName, Introduce, StartPrice, UID)
	cursor.execute(sql, param)
	conn.commit()
	return 

#刪除跟修改
	
def delete(pid):  #刪除商品
	sql='''
	DELETE product, record
    FROM product
    LEFT JOIN record ON product.pid = record.pid
    WHERE product.pid = %s;'''
	
	cursor.execute(sql, (pid,))
	conn.commit()
	return

def edit(ProductName, Introduce, StartPrice, pid):  #修改商品資料
	sql='''
	update `product` 
	set 
		ProductName = %s, 
		Introduce = %s, 
		StartPrice = %s 
	where pid = %s;'''
	param=(ProductName, Introduce, StartPrice, pid)
	cursor.execute(sql,param)
	conn.commit()
	return
	

#找資料


def product(): # 找全部的商品
    sql="""
	SELECT 
		product.pid,
		product.ProductName, 
		product.Introduce, 
		product.StartPrice,
		product.StartPrice , 
		user.UserName, 
		product.AddTime,
		greatest(ifnull(max(record.BidPrice), product.StartPrice), product.StartPrice) as price
	FROM `product` 
	LEFT JOIN user ON user.UID = product.UID
	left join record on record.pid = product.pid
	group by product.pid;"""
    
    cursor.execute(sql)
    return cursor.fetchall()

def my_product(UID):  # 找 user 的商品（首頁）
	sql="""
	SELECT 
		user.UID, 
		product.pid,
		product.ProductName, 
		product.Introduce, 
		product.StartPrice,
		product.AddTime,
		product.StartPrice, 
		greatest(ifnull(max(record.BidPrice), product.StartPrice), product.StartPrice) as price
	from `product`
	left join `record` on product.pid=record.pid
	left join `user` on product.UID=user.UID 
	where product.UID=%s
	group by product.pid;"""
	param = (UID,)
	cursor.execute(sql, param)
	return cursor.fetchall()

def select_product(pid): # 找單一商品（用在出價、修改）
	sql="""
	SELECT 
		product.pid, 
		product.ProductName, 
		product.Introduce, 
		product.StartPrice, 
		greatest(ifnull(max(record.BidPrice), product.StartPrice), product.StartPrice) as price, 
		record.BidPrice,
		user.UserName, 
		product.AddTime
	from `product` 
	left join `record` on record.pid=product.pid
	left join `user` on product.UID=user.UID 
	where product.pid=%s 
	group by product.pid"""
	param = (pid,)
	cursor.execute(sql, param)
	return cursor.fetchall()

def get_record(pid): #找出價記錄
	sql="""
	SELECT 
		product.pid, 
		record.UID,
		product.ProductName, 
		product.Introduce, 
		product.StartPrice, 
		greatest(ifnull(max(record.BidPrice), product.StartPrice), product.StartPrice) as NowPrice, 
		record.BidPrice,
		NP.NowPrice,
		record.BidTime,
		sell.UserName as S_user,
		bid.UserName as B_user,
		product.AddTime,
		record.BidPrice - ifnull(lag(record.BidPrice) over (order by rid), product.StartPrice) as addPrice
	from `product` 
		LEFT JOIN (
    	SELECT 
        	product.pid,
        	greatest(ifnull(max(record.BidPrice), product.StartPrice), product.StartPrice) AS NowPrice
    	FROM `product`
    		LEFT JOIN `record` ON record.pid = product.pid
    	GROUP BY product.pid
			) AS NP ON NP.pid = product.pid
		left join `record` on record.pid = product.pid
		left join `user` as `sell` on sell.UID = product.UID 
		left join `user` as `bid` on record.UID = bid.UID
	where product.pid=%s 
	
	group by 
		product.pid,
		record.BidTime
	
	order by 
		record.BidPrice
	desc;"""
	# left join `user` as `sell` on sell.UID = product.UID 找賣家資料
	# left join `user` as `bid` on record.UID = bid.UID 找出價者資料
	param = (pid,)
	cursor.execute(sql, param)
	return cursor.fetchall()


