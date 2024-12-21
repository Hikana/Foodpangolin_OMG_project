from functools import wraps
from flask import Flask, redirect, render_template, request, session
import dbUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = '123TyU%^&'

url_role_map = {
    1: "/store",
    2: "/customer",
    3: "/delivery",
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
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/store', methods=['GET'])
@login_required
@role_check
def store():
    return render_template('store.html')


@app.route('/customer', methods=['GET'])
@login_required
@role_check
def customer():
    return render_template('customer.html')

@app.route('/customer/store/<int:store_id>', methods=['GET'])
@login_required
@role_check
def customer_stroe(store_id):
    print(store_id)
    
    return render_template('customer_store.html')


@app.route('/delivery', methods=['GET'])
@login_required
@role_check
def delivery():
    return render_template('delivery.html')


# api
@app.route('/login', methods=['POST'])
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


@app.route('/store-list', methods=['GET'])
def api_store_list():
    store_list = dbUtils.get_store_list()
    return {"data": store_list}

@app.route('/store-list/<int:store_id>/menu', methods=['GET'])
def api_store_menu(store_id):
    store_menu = dbUtils.get_store_menu(store_id)
    return {"data": store_menu}

@app.route('/store-list/<int:store_id>/order', methods=['POST'])
def api_store_order(store_id):
    # 品項、數量、單價
    # 先撈出 customer_id
    print(session['id'])
    customer_id = dbUtils.get_customer_id(session['id'])[0]["id"]
    print(customer_id)
    # 再寫入 customer_order

    customer_order = dbUtils.add_customer_order(customer_id, store_id)
    return 


if __name__ == '__main__':
    app.run(debug=True)
