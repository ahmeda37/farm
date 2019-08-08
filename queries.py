from main import mysql
#Sale_Orders-------------------------------------
def setOrder(id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO sale_orders (cid) VALUES("+id+");")
    mysql.connection.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getOrders():
    cur = mysql.connection.cursor()
    cur.execute("select sale_orders.oid, customers.name, sale_orders.total, sale_orders.reg_date from sale_orders inner join customers on sale_orders.cid = customers.cid where sale_orders.paid = 0")
    mysql.connection.commit()
    myresult = cur.fetchall()
    return myresult
def deleteOrder(value):
    cur = mysql.connection.cursor()
    cur.execute("DELETE from single_order where oid ="+str(value)+"")
    mysql.connection.commit()
    cur.execute("DELETE FROM sale_orders where oid ="+str(value)+"")
    mysql.connection.commit()
def getTotal(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT total from sale_orders where oid ="+str(id)+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
def updateTotal(value,id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE sale_orders SET total="+str(value)+" where oid ="+id+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
#Single_Order------------------------------------
def saveItem(item,id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO single_order (oid,pid,price,quantity) VALUES ("+str(id)+","+str(item['id'])+","+str(item['price'])+","+str(item['quantity'])+")")
    mysql.connection.commit()
    cur.execute("SELECT * from single_order where oid="+id+" and pid="+item['id']+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getItem(value):
    cur = mysql.connection.cursor()
    cur.execute("SELECT price,quantity from single_order where singleid="+value+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def deleteItem(value):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM single_order where singleid ="+value+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
#Sale_Orders Join Single_Order--------------------
def getOrderItems(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT products.pid, products.name, single_order.singleid, single_order.price, single_order.quantity from single_order inner join products on products.pid = single_order.pid where single_order.oid = "+str(id)+"")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult

def paidOrder(oid,cid):
    cur = mysql.connection.cursor()
    cur.execute("INSERT into sale_invoices (oid,cid) values ("+oid+","+cid+")")
    mysql.connection.commit()
    cur.execute("UPDATE sale_orders SET paid = 1 where oid="+oid+"")
    mysql.connection.commit()
    cur.close()

def getInvoices():
    cur = mysql.connection.cursor()
    cur.execute("select sale_invoices.inid, customers.name, sale_orders.total, sale_invoices.reg_date from sale_invoices inner join customers on sale_invoices.cid = customers.cid inner join sale_orders on sale_invoices.oid = sale_orders.oid")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult