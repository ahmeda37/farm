#Customers--------------------------------------
def getCustomer(id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers where cid="+id)
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getCustomers(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult
#Products----------------------------------------
def getProducts(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult
#Sale_Orders-------------------------------------
def setOrder(id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO sale_orders (cid) VALUES("+id+");")
    mysql.connection.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getOrders(mysql):
    cur = mysql.connection.cursor()
    cur.execute("select sale_orders.oid, customers.name, sale_orders.total, sale_orders.reg_date from sale_orders inner join customers on sale_orders.cid = customers.cid")
    mysql.connection.commit()
    myresult = cur.fetchall()
    return myresult
def deleteOrder(value,mysql):
    cur = mysql.connection.cursor()
    cur.execute("DELETE from single_order where oid ="+str(value)+"")
    mysql.connection.commit()
    cur.execute("DELETE FROM sale_orders where oid ="+str(value)+"")
    mysql.connection.commit()
def getTotal(id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT total from sale_orders where oid ="+str(id)+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
def updateTotal(value,id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE sale_orders SET total="+str(value)+" where oid ="+id+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
#Single_Order------------------------------------
def saveItem(item,id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO single_order (oid,pid,price,quantity) VALUES ("+str(id)+","+str(item['id'])+","+str(item['price'])+","+str(item['quantity'])+")")
    mysql.connection.commit()
    cur.execute("SELECT * from single_order where oid="+id+" and pid="+item['id']+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getItem(value,mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT price,quantity from single_order where singleid="+value+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
def deleteItem(value,mysql):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM single_order where singleid ="+value+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    return myresult
#Sale_Orders Join Single_Order--------------------
def getOrderItems(id,mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT products.pid, products.name, single_order.singleid, single_order.price, single_order.quantity from single_order inner join products on products.pid = single_order.pid where single_order.oid = "+str(id)+"")
    mysql.connection.commit()
    myresult = cur.fetchall()
    return myresult
