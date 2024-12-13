from flask import Flask, render_template, request, session, redirect
from functools import wraps
from tkinter import messagebox
from dbUtils import product, login, my_product, select_product, add_price, get_record, add_product, edit, delete

app = Flask(__name__, static_folder='templates', static_url_path='/')
app.config['SECRET_KEY'] = '123TyU%^&'


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if not session.get('loginID'):
            return redirect('/loginPage')
        return f(*args, **kwargs)
    
    return wrapper


@app.route('/loginPage', methods=['GET', 'POST']) #登入頁面
def login_page():
    if request.method == 'POST':

        form = request.form
        account = form.get('account')
        password = form.get('PWD')

        user = login(account, password)  
        if user:
            user_info = user[0]
            session['loginID'] = user_info['account']
            session['UserName'] = user_info['UserName']
            session['UID'] = user_info['UID']
            return redirect("/Home")
        else:
            return render_template('loginPage.html', error = '帳號或密碼錯誤')

    # 若是 GET 請求，直接出現登入頁面
    return render_template('loginPage.html')



@app.route('/logout') #登出
def logout():

    session.clear()  # 清除所有 session 資料

    return redirect('/loginPage')



@app.route('/Home') #首頁
@login_required
def home():

    user_name = session.get('UserName', ' ') # 將資料從 session 抓出來，沒有資料就顯示空白
    product_list = product()

    return render_template('HomePage.html', userName=user_name, products=product_list)



@app.route('/bidding/<int:pid>', methods=['GET','POST']) # 出價
@login_required
def Bid(pid):

    user_name = session.get('UserName')
    product_info = select_product(pid) # 單一商品的資訊
    
    if request.method == 'POST':
        BidPrice = int(request.form['bid_price']) # 從 form get 出價
        UID = session.get('UID') # 出價的用戶
    
        add_price(pid, BidPrice, UID)
        return redirect('/Home')
    
    
    #add_price = int(request.form['add_price'])
    return render_template('BidPage.html', userName=user_name, product_i=product_info)


@app.route('/add_product', methods = ['GET','POST']) #新增商品
@login_required
def AddProduct():

    user_name = session.get('UserName')

    if request.method=='POST':
        ProductName = str(request.form['P_name'])
        Introduce = str(request.form['P_introduce'])
        StartPrice = int(request.form['P_price'])
        UID = session.get('UID')
        add_product(ProductName, Introduce, StartPrice, UID)
        return redirect('/self_page')
    
    return render_template('AddPage.html', userName=user_name)
    


@app.route('/self_page', methods=['GET','POST']) #個人頁
@login_required
def self():

    user_name = session.get('UserName', ' ')
    UID = session.get('UID')
    MP=my_product(UID) #商品

    if request.method=='POST': #刪除商品
        pid = int(request.form['pid'])
        delete(pid)
        return redirect('/self_page')
   
    
    return render_template('SelfPage.html', userName=user_name, myProduct=MP)



@app.route('/record_page/<int:pid>', methods=['GET']) #出價記錄
@login_required
def record(pid):
    user_name = session.get('UserName', ' ')
    p_record=get_record(pid) #商品出價記錄
    return render_template('RecordPage.html', userName=user_name, Record=p_record)




    

@app.route('/edit_product/<int:pid>', methods=['GET','POST']) #修改商品
@login_required
def Edit(pid):
    
    user_name = session.get('UserName')
    PI = select_product(pid)

    if request.method == 'POST':
        ProductName = str(request.form['P_name'])
        Introduce = str(request.form['P_introduce'])
        StartPrice = int(request.form['P_price']) 
        pid = int(request.form['pid'])
        edit(ProductName, Introduce, StartPrice, pid)
        return redirect('/self_page')
    
    return render_template('EditPage.html', userName=user_name, product_i = PI)




if __name__ == "__main__":
    app.run(debug=True)
