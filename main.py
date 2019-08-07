from livereload import Server
from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from config import user,password,db,host
from werkzeug.security import generate_password_hash
from flask_login import LoginManager,current_user,login_user,logout_user
import datetime
import queries

app = Flask(__name__)
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
app.config['MYSQL_HOST'] = host
mysql = MySQL(app)
login = LoginManager(app)

from models import user

open_order = False
curCID = 0
curOID = 0
total=0

@app.route('/signup',methods=['POST','GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        result = request.form
        if user.get_user(result['username']) is None:
            newUser = user.User()
            newUser.User(username=result['username'],password=result['password'])
            user.add_user(newUser)
    return render_template('signup.html')

@app.route('/',methods =['POST','GET'])
def index():
    global total
    #user = User.User()
    #user.set_password('secret')
    #print(user.check_password('seet'))
    if request.method == 'POST':
        result = request.form
        item = {
            'id':result['item-name'][:1],
            'name':result['item-name'][2:],
            'price':result['price'],
            'quantity':result['quantity'],
            'total':total+int(result['price']) * int(result['quantity'])
        }
        myresult = queries.saveItem(item,curOID)
        queries.updateTotal(item['total'],curOID)
        total = item['total']
    if open_order == True:
        queries.updateTotal(total,curOID)
        return render_template('index.html',customer=queries.getCustomer(curCID),items=queries.getProducts(),result=queries.getOrderItems(curOID),total=total,curOID=curOID)
    return render_template('index.html',customers=queries.getCustomers(),items=queries.getProducts(), result=queries.getOrderItems(curOID),total=total)

@app.route('/delete/<value>',methods=['GET'])
def delete_item(value):
    global total
    value = int(value)
    price = queries.getItem(str(value))
    total = total - (price[0]*price[1])
    queries.deleteItem(str(value))
    queries.updateTotal(total,curOID)
    return redirect("/")

@app.route('/orders',methods=['GET'])
def showOrders():
    global open_order
    global total
    open_order = False
    total = 0
    orders = queries.getOrders()
    ttotal = 0
    for key in orders:
        ttotal = ttotal + key[2]
    return render_template('sale_orders.html',orders=orders,total=ttotal)

@app.route('/orders/update/<id>',methods=['GET'])
def update_Order(id):
    global open_order
    global curCID
    global curOID
    global total
    print(type(id))
    open_order = True
    curOID = str(id)
    curCID = str(queries.getCustomerBySO(id)[0])
    total = int(queries.getTotal(curOID)[0])
    return render_template('index.html',customer=queries.getCustomer(curCID),items=queries.getProducts(),result=queries.getOrderItems(curOID),total=total,curOID=curOID)

@app.route('/orders/delete/<id>',methods=['GET'])
def delete_Order(id):
    queries.deleteOrder(id)
    return redirect('/orders')

@app.route('/invoices',methods=['GET','POST'])
def showInvoices():
    global open_order
    global total
    if request.method == 'POST':
        result = request.form
        myresult = queries.paidOrder(curOID,curCID)
        return redirect('/invoices')
    open_order = False
    total = 0
    ttotal = 0
    myresult = queries.getInvoices()
    print(myresult)
    for key in myresult:
        ttotal = ttotal + key[2] 
    return render_template('invoice.html',orders=myresult,total=ttotal)
@app.route('/setCustomer/<id>',methods=['GET'])
def setCustomer(id):
    global open_order
    global curCID
    global curOID
    if (open_order != True):
        curCID = str(queries.getCustomer(id)[0])
        curOID = str(queries.setOrder(id)[0])
        open_order = True
    return redirect('/')

@app.route('/add',methods=['GET'])
def add():
    print(request)
    return render_template('add.html')
@app.route('/add/customer',methods=['POST'])
def addCustomer():
    if request.method == 'POST':
        result = request.form
        myresult = queries.addCustomer(result['name'],result['address'])
    return redirect('/add/customer/success')
@app.route('/add/customer/success', methods=['GET'])
def addCustomerSuccess():
    return render_template('add.html',alert="Custoemr has been added")

@app.route('/add/product',methods=['POST'])
def addProduct():
    if request.method == 'POST':
        result = request.form
        myresult = queries.addProduct(result['name'])
    return redirect('/add/product/success')
@app.route('/add/product/success',methods=['GET'])
def addProductSuccess(): 
    return render_template('add.html',alert='Product has been added')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        print('signed in')
    #if request.method == 'POST':
    curUser = user.get_user('ahmed')
    if curUser is None or not user.check_password('secret'):
        print('Invalid username or password')
    else:
        login_user(user)
    print(curUser)
    return redirect('/')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.debug=True
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(debug='True')