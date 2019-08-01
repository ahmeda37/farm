from livereload import Server
from flask import Flask, render_template,request, redirect
from flask_mysqldb import MySQL
from config import user,password,db,host
import datetime
app = Flask(__name__)
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
app.config['MYSQL_HOST'] = host
mysql = MySQL(app)

open_order = False
curCID = 0
curOID = 0
order={}
count=0
total=0
orders={}
counter=0

def getProducts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult

def getCustomers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers where cid="+id)
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def setOrder(id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO sale_orders (cid) VALUES("+id+");")
    mysql.connection.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def saveItem(item):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO single_order VALUES ("+str(curOID)+","+str(item['id'])+","+str(item['price'])+","+str(item['quantity'])+")")
    mysql.connection.commit()
    cur.execute("SELECT * from single_order where oid="+curOID+" and pid="+item['id']+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getOrderItems():
    cur = mysql.connection.cursor()
    cur.execute("SELECT products.pid, products.name, single_order.price, single_order.quantity from single_order inner join products on products.pid = single_order.pid where single_order.oid = "+curOID+"")
    mysql.connection.commit()
    myresult = cur.fetchall()
    return myresult

@app.route('/',methods =['POST','GET'])
def index():
    global count
    global total
    global order
    if request.method == 'POST':
        result = request.form
        item = {
            'id':result['item-name'][:1],
            'name':result['item-name'][2:],
            'price':result['price'],
            'quantity':result['quantity'],
            'total':int(result['price']) * int(result['quantity'])
        }
        myresult = saveItem(item)
        #print(item)
        #print(myresult)
        order = getOrderItems();
        #print(order)
        #count +=1
        total += item['total']
    if open_order == True:
        return render_template('index.html',customer=getCustomer(curCID),items=getProducts(),result=order,total=total,curOID=curOID)
    return render_template('index.html',customers=getCustomers(),items=getProducts(), result=order,total=total)

@app.route('/delete/<value>',methods=['GET'])
def delete_item(value):
    global count
    global total
    value = int(value)
    total = total - int(order[value]['total'])
    count -= 1
    del order[value]
    return redirect("/")

@app.route('/save/<sale_order>',methods=['POST'])
def save_order(sale_order):
    global count
    global total
    global order
    global orders
    global counter
    if(count > 0):
        item={
            'order':order,
            'count':count,
            'this_dict':this_dict
        }
        orders.update({counter:item})
        counter += 1
    count = 0
    total = 0
    order = {}
    return redirect("/orders")

@app.route('/orders',methods=['GET'])
def showOrders():
    print(orders)
    return render_template('sale_orders.html',orders=orders)

@app.route('/setCustomer/<id>',methods=['GET'])
def setCustomer(id):
    global open_order
    global curCID
    global curOID
    if (open_order != True):
        curCID = str(getCustomer(id)[0])
        #print(customer[0])
        curOID = str(setOrder(id)[0])
        #print(myOrder[0])
        open_order = True
    return redirect('/')

if __name__ == '__main__':
    app.debug=True
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(debug='True')