from functools import wraps
from flask import Flask, redirect, render_template, request, session
import dbUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = '123TyU%^&'

url_role_map = {
    1: "/store",
    2: "/customer",
    3: "/delivery",
    4: "/platform",
}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if not session.get('loginID'):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper


def role_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if not request.path.startswith(url_role_map[session.get('role')]) :
            return redirect('/login')
        
        return f(*args, **kwargs)

    return wrapper

# 預設情況下，Flask 會使用 "./static" 資料夾作為靜態資源
# page
@app.route('/')
def role_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if not request.path.startswith(url_role_map[session.get('role')]) :
            return redirect('/login')
        
        return f(*args, **kwargs)

    return wrapper

# 預設情況下，Flask 會使用 "./static" 資料夾作為靜態資源
# page
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


#================================================
@app.route('/store', methods=['GET'])  # 店家首頁
@login_required
@role_check
def store():
    data = dbUtils.get_store_self_order_list(session['id'])
    print(session['id'])
    return render_template('store.html',data = data, sid=session['id'])

#================================================
@app.route('/customer', methods=['GET']) # 客戶首頁
@login_required
@role_check
def customer():
    return render_template('customer.html')

#================================================
@app.route('/delivery', methods=['GET']) # 送貨員首頁
@login_required
@role_check
def delivery():
    return render_template('delivery.html')

#================================================
@app.route('/platform', methods=['GET']) # 送貨員首頁
@login_required
@role_check
def platform():
    data = dbUtils.get_all_users()
    print(session['id'],"dddeeedddeeedddeee===>?>>")
    return render_template('platform.html',data = data)
#================================================
@app.route('/customer/store/<int:store_id>', methods=['GET']) 
@login_required
@role_check
def customer_stroe(store_id):
    print(store_id)
    
    return render_template('customer_store.html')

@app.route('/delivery/order/<int:order_id>', methods=['GET']) 
@login_required
@role_check
def delivery_order(order_id):
    print(order_id)
    data = dbUtils.get_customer_order(order_id)
    return render_template('delivery_order.html',data = data)

@app.route('/store/menu/<int:menu_id>', methods=['GET']) 
@role_check
def store_menu(menu_id):
    print(menu_id)
    return render_template('store_menu.html')

#================================================
# api
@app.route('/login', methods=['POST']) # 登入（所有人）
def api_login():
    
    form = request.json
    username = form.get('username')
    password = form.get('password')
    user = dbUtils.login(username, password)
    if user :
        user_info = user[0]
        session['loginID'] = user_info['username']
        session['role'] = user_info['role']
        session['id'] = user_info['id']
        return {"url": url_role_map[user_info['role']]}
    return {"url": "/login"}

#================================================
# 顧客頁面
@app.route('/store-list', methods=['GET']) # 列出商店資訊（顧客）
def api_store_list():
    store_list = dbUtils.get_store_list()
    return {"data": store_list}

@app.route('/store-list/<int:store_id>/menu', methods=['GET']) # 列出選取商店的菜單（顧客）
def api_store_menu(store_id):
    store_menu = dbUtils.get_store_menu(store_id)
    return {"data": store_menu}

@app.route('/store-list/<int:store_id>/order', methods=['POST']) # 顧客點餐（顧客）
def api_store_order(store_id):
    # 品項、數量、單價、目的地
    # 先撈出 customer_id
    customer_id = dbUtils.get_customer_id(session['id'])[0]["id"]
    
    # 從 request 取得 destination 放入 customer_order
    form = request.json
    destination = form.get('order')[0]["destination"]
    order = form.get('order')[0]["name"]    
    # 再寫入 customer_order

    # 取得剛寫入的 customer_order 資料的 id
    customer_order_id = dbUtils.add_customer_order(customer_id, store_id, destination)
    # 還有整理從 request 取得的訂單內容
    # 查找 store menu 找對應餐點的 id
    order_id = dbUtils.get_menu_order(order)['id']
    # 再寫入 order_menu 中
    add_order = dbUtils.add_order_menu(order_id, customer_order_id)
    return {"data": customer_order_id}

#================================================
# 送貨員頁面
@app.route('/order-list', methods=['GET']) # 待送清單跟已接訂單（送貨員）
def api_order_list():
    order_list = dbUtils.get_available_order()
    print("================",order_list)
    delivery_id = dbUtils.get_delivery_id(session['id'])[0]["id"]
    print("+++++++++++++++",delivery_id)
    delivery_list = dbUtils.get_delivery_order_list(delivery_id)
    print("***********************",delivery_list)
    print(order_list,"sb=====================sb")
    return {"data": order_list, "order": delivery_list}

@app.route('/order-list/<int:order_menu_id>', methods=['GET']) # 待送清單詳細（送貨員）
def api_customer_order(order_menu_id):
    print("==========確定進入路由")
    status = request.args["change_status"]
    customer_order = dbUtils.get_customer_order(order_menu_id)
    delivery_id = dbUtils.get_delivery_id(session['id'])[0]["id"]
    dbUtils.edit_customer_delivery(delivery_id, order_menu_id,status)
    
    # 到最後一步，訂單完成 => status4 影響 platf
    if status == "4":
        a = dbUtils.get_price(customer_order[0]['id'])
        order_all = dbUtils.get_customer_all_order(order_menu_id)
        print("////////////////////////////",order_all)
        dbUtils.edit_sumry(order_all[0]['customer_id'], order_all[0]['store_id'], order_all[0]['delivery_id'], a['price'])

    print("---------------------",customer_order)   
    return {"data": customer_order}

# @app.route('/order-list/<string:order_menu_id>', methods=['POST']) # 接單（送貨員）
# def api_customer_delivery(order_menu_id):
#     delivery_id = dbUtils.get_delivery_id(session['id'])[0]["id"]
#     customer_delivery = dbUtils.edit_customer_delivery(delivery_id, order_menu_id)
#     return {"data": customer_delivery}


#================================================
# 商店頁面
@app.route('/menu-list', methods=['GET']) # 商店菜單
def api_store_self_menu():
    store_menu = dbUtils.get_store_menu(session['id'])
    return {"data": store_menu}

@app.route('/menu-order-list', methods=['GET']) # 商店拿取order部分
def api_store_self_order():
    store_order = dbUtils.get_store_self_order_list(session['id'])
    print(store_order,"nignaignnagingianignai")
    return {"data": store_order}

@app.route('/menu-order-complete',methods=['GET']) # 完成訂單的部分
def api_complete_status():
    oid = request.args['id']
    store_order = dbUtils.meal_status_complete(oid)
    print(store_order,"=d=d=d==d=d=d=d=d=d=")
    return {"data": store_order}












#---------------------------------------------------------------------------------------------------------------
# 新增路由
@app.route('/view_menu',methods=['GET']) #查看菜單
def vmenu():
    sid = session['id']
    data = dbUtils.store_own_list(sid)
    return render_template('/menu.html', data=data, sid=sid)


@app.route('/addfoodUI',methods=['GET']) #跳轉至新增菜單UI
def addmenu():
    return render_template('/addfoodUI.html')

@app.route('/add',methods=['POST']) #新增菜單
def add():
    form = request.form
    sid = session['id']
    name = form['name']
    price = form['price']
    intro = form['intro']
    dbUtils.add_food(name, price, intro, sid)
    return redirect('/view_menu')


@app.route('/fixfoodUI',methods=['POST', 'GET']) #跳轉至修改菜單UI
def fix():
    sid = session['id']
    food_id = request.args['food_id']
    data = dbUtils.the_food(food_id)
    return render_template('/fixfoodUI.html', data=data, sid=sid, food_id=food_id)

@app.route('/fix',methods=['POST']) #修改菜單
def fixmenu():
    form = request.form
    food_id=form['food_id']
    name = form['name']
    price = form['price']
    intro = form['intro']
    print(name, price, intro, food_id)
    dbUtils.fix_food(name, price, intro, food_id)
    return redirect('/view_menu')


@app.route('/dele',methods=['GET'])
def dele():
    food_id = request.args['food_id']
    dbUtils.dele_food(food_id)
    return redirect('/view_menu')















if __name__ == '__main__':
    app.run(debug=True)
