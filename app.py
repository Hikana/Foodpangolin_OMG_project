from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for
import dbUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = '123TyU%^&'

url_role_map = {
    1: "/store",
    2: "/customer",
    3: "/delivery",
    4: "/platform",
}

order_status = {
    0:"製作中",
    1:"待運送",
    2:"運送中",
    3:"已送達",
    4:"已簽收"
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
# api
@app.route('/login', methods=['POST']) # 登入（所有人）
def api_login():
    
    username = request.form.get('username')
    password = request.form.get('password')
    user = dbUtils.login(username, password)
    if user :
        user_info = user[0]
        session['loginID'] = user_info['username']
        session['role'] = user_info['role']
        session['id'] = user_info['id']
        return redirect(url_role_map.get(user_info['role'],'/'))
    return redirect('/login')

#================================================
# 客戶頁面
@app.route('/customer', methods=['POST','GET']) # 客戶首頁 ##
@login_required
@role_check
def api_store_list():
    customer_id = dbUtils.get_customer_id(session['id'])[0]["id"]
    if request.method == 'POST':
        form = request.form
        oid = form['oid']
        dbUtils.edit_customer_order(oid)
    store_list = dbUtils.get_store_list()
    order_list = dbUtils.get_customer_self_order(customer_id) # 顧客點的菜
    return render_template('customer.html',data=store_list,order=order_list)


@app.route('/store-menu', methods=['GET']) # 列出選取商店的菜單（顧客） ##
def api_store_menu():
    store_id = request.args['store_id']
    store_menu = dbUtils.get_store_menu(store_id)
    return render_template('customer_store.html', data=store_menu)

@app.route('/order', methods=['POST','GET']) # 顧客點餐，一次一個餐點（顧客） ##
def api_store_order():
    # 品項、數量、單價、目的地
    # 先撈出 customer_id
    
    if request.method == 'GET':
        menu_id = request.args['menu_id']
        store_menu = dbUtils.get_menu(menu_id)
        
    if request.method == 'POST':
        menu_id = request.form['menu_id']
        store_menu = dbUtils.get_menu(menu_id)
        form = request.form 
        customer_id = dbUtils.get_customer_id(session['id'])[0]["id"]
        # 從 request 取得 destination 放入 customer_order
        
        destination = form['destination']
        order = form['order']   
        quantity = form['quantity']
        store_id = form['store_id']

        # 再寫入 customer_order

        # 取得剛寫入的 customer_order 資料的 id
        customer_order_id = dbUtils.add_customer_order(customer_id, store_id, quantity, destination)
        # 還有整理從 request 取得的訂單內容
        # 查找 store menu 找對應餐點的 id
        order_id = dbUtils.get_menu_order(order)['id']
        # 再寫入 order_menu 中
        dbUtils.add_order_menu(order_id, customer_order_id)
        return redirect(f'/store-menu?store_id={store_id}')
    return render_template('customer_order.html', data=store_menu, menu_id=menu_id)

@app.route('/customer_comment', methods=['GET']) # 顧客可以評價的訂單
def get_customer_finish_order():
    customer_id = dbUtils.get_customer_id(session['id'])[0]["id"]
    order = dbUtils.get_customer_finish_order(customer_id)
    return render_template('customer_comment.html', order=order)

@app.route('/order_comment', methods=['GET','POST']) # 顧客對訂單的評價
def add_customer_comment():
    if request.method =='POST':
        form = request.form
        order_id = form['oid']
        comment = form['comment']
        rating = form['rating']
        dbUtils.add_customer_comment(order_id, rating, comment)
        return redirect('/customer_comment')
    order_id = request.args['oid']
    order_intro = dbUtils.get_order_intro(order_id)
    return render_template('/order_comment.html', data=order_intro)






#================================================

# 送貨員頁面
@app.route('/delivery', methods=['GET','POST']) # 送貨員首頁 ##
@login_required
@role_check
def delivery():
    order_list = dbUtils.get_available_order() # 可以接的訂單
    delivery_id = dbUtils.get_delivery_id(session['id'])[0]["id"]
    # delivery_list = dbUtils.get_delivery_order_list(delivery_id) # 已經接的訂單
    if request.method == 'POST':
        form = request.form
        order_id = form['order_id']
        status = 2
        dbUtils.edit_customer_delivery(delivery_id, status, order_id)
        return redirect('/delivery')
    return render_template('delivery.html', order=order_list)


@app.route('/delivery-order', methods=['GET','POST']) # 送貨員已接訂單頁面 ##
@login_required
@role_check
def api_get_delivery_order():
    delivery_id = dbUtils.get_delivery_id(session['id'])[0]["id"]
    delivery_list = dbUtils.get_delivery_order_list(delivery_id) # 已經接的訂單
    if request.method == 'POST':
        form = request.form
        order_id = form['order_id']
        status = 3
        dbUtils.edit_customer_delivery(delivery_id, status, order_id) # 已送達更改狀態
        return redirect('/delivery-order')
    return render_template('delivery_order.html', order=delivery_list)





# 店家頁面
@app.route('/store', methods=['GET','POST'])  # 店家首頁 ##
@login_required
@role_check
def store():
    store_id = dbUtils.get_store_id(session['id'])[0]["id"]
    status=0
    data = dbUtils.get_store_self_order_list(store_id,status) 
    
    return render_template('store.html',data = data)



@app.route('/view_menu',methods=['GET']) # 查看菜單 ##
def api_get_store_menu():
    sid = dbUtils.get_store_id(session['id'])[0]["id"]
    data = dbUtils.get_store_own_list(sid)
    return render_template('/menu.html', data=data, sid=sid)



@app.route('/addfoodUI',methods=['GET']) # 跳轉至新增菜單UI ##
def add_menu():
    return render_template('/addfoodUI.html')


@app.route('/add',methods=['POST']) # 新增菜單 ##
def add_store_menu():
    form = request.form
    sid = dbUtils.get_store_id(session['id'])[0]["id"]
    name = form['name']
    price = form['price']
    intro = form['intro']
    dbUtils.add_food(name, price, intro, sid)
    return redirect('/view_menu')


@app.route('/menu-order-complete',methods=['GET']) 
def edit_status():
    customer_order_id=request.args['id']
    print(customer_order_id)
    dbUtils.edit_status(customer_order_id)
    return redirect('/store')



@app.route('/fixfoodUI',methods=['POST', 'GET']) # 跳轉至修改菜單UI ##
def fix():
    sid = session['id']
    food_id = request.args['food_id']
    data = dbUtils.get_menu_intro(food_id)
    return render_template('/fixfoodUI.html', data=data, food_id=food_id)

@app.route('/fix',methods=['POST']) #修改菜單
def fix_menu():
    form = request.form
    print("-----------------------",form)
    food_id=form['food_id']
    name = form['name']
    price = form['price']
    intro = form['intro']
    # print(name, price, intro, food_id)
    dbUtils.fix_food(name, price, intro, food_id)
    return redirect('/view_menu')


@app.route('/delet',methods=['GET'])
def delet():
    food_id = request.args['food_id']
    dbUtils.dele_food(food_id)
    return redirect('/view_menu')


@app.route('/platform', methods=['GET']) # 平台首頁
@login_required
@role_check
def platform():
    data = dbUtils.get_all_users()
    print(session['id'])
    return render_template('platform.html',data = data)





#---------------------------------------------------------------------------------------------------------------
# 新增路由 菜單編輯跟刪除













if __name__ == '__main__':
    app.run(debug=True)
