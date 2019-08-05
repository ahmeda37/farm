from livereload import Server
from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from config import user,password,db,host
import datetime
import queries
app = Flask(__name__)
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
app.config['MYSQL_HOST'] = host
mysql = MySQL(app)

open_order = False
curCID = 0
curOID = 0
total=0

@app.route('/',methods =['POST','GET'])
def index():
    global total
    if request.method == 'POST':
        result = request.form
        item = {
            'id':result['item-name'][:1],
            'name':result['item-name'][2:],
            'price':result['price'],
            'quantity':result['quantity'],
            'total':total+int(result['price']) * int(result['quantity'])
        }
        myresult = queries.saveItem(item,curOID,mysql)
        queries.updateTotal(item['total'],curOID,mysql)
        total = item['total']
    if open_order == True:
        queries.updateTotal(total,curOID,mysql)
        return render_template('index.html',customer=queries.getCustomer(curCID,mysql),items=queries.getProducts(mysql),result=queries.getOrderItems(curOID,mysql),total=total,curOID=curOID)
    return render_template('index.html',customers=queries.getCustomers(mysql),items=queries.getProducts(mysql), result=queries.getOrderItems(curOID,mysql),total=total)

@app.route('/delete/<value>',methods=['GET'])
def delete_item(value):
    global total
    value = int(value)
    price = queries.getItem(str(value),mysql)
    total = total - (price[0]*price[1])
    queries.deleteItem(str(value),mysql)
    queries.updateTotal(total,curOID,mysql)
    return redirect("/")

@app.route('/orders',methods=['GET'])
def showOrders():
    global open_order
    global total
    open_order = False
    total = 0
    orders = queries.getOrders(mysql)
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
    curCID = str(queries.getCustomerBySO(id,mysql)[0])
    total = int(queries.getTotal(curOID,mysql)[0])
    return render_template('index.html',customer=queries.getCustomer(curCID,mysql),items=queries.getProducts(mysql),result=queries.getOrderItems(curOID,mysql),total=total,curOID=curOID)



@app.route('/orders/delete/<id>',methods=['GET'])
def delete_Order(id):
    queries.deleteOrder(id,mysql)
    return redirect('/orders')

@app.route('/setCustomer/<id>',methods=['GET'])
def setCustomer(id):
    global open_order
    global curCID
    global curOID
    if (open_order != True):
        curCID = str(queries.getCustomer(id,mysql)[0])
        curOID = str(queries.setOrder(id,mysql)[0])
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
        myresult = queries.addCustomer(mysql,result['name'],result['address'])
    return redirect('/add/customer/success')
@app.route('/add/customer/success', methods=['GET'])
def addCustomerSuccess():
    return render_template('add.html',alert="Custoemr has been added")

@app.route('/add/product',methods=['POST'])
def addProduct():
    if request.method == 'POST':
        result = request.form
        myresult = queries.addProduct(mysql,result['name'])
    return redirect('/add/product/success')
@app.route('/add/product/success',methods=['GET'])
def addProductSuccess(): 
    return render_template('add.html',alert='Product has been added')

if __name__ == '__main__':
    app.debug=True
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(debug='True')