from main import mysql

class Customer():
	def Customer(self,name,address):
		self.name = name
		self.address = address
	def get_name(self):
		return self.name
	def get_address(self):
		return self.address
	def set_cid(self,cid):
		self.cid = cid
	def get_cid(self):
		return self.cid

def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers where cid="+str(id))
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    customer = Customer()
    customer.Customer(myresult[1],myresult[2])
    customer.set_cid(myresult[0])
    return customer
def getCustomerBySO(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT cid FROM sale_orders where oid="+str(id)+"")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult
def getCustomers():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM customers")
	mysql.connection.commit()
	myresult = cur.fetchall()
	cur.close()
	return myresult
def addCustomer(customer):
    cur = mysql.connection.cursor()
    cur.execute("INSERT into customers (name,address) VALUES ('"+customer.name+"','"+customer.address+"')")
    mysql.connection.commit()
    cur.execute("Select last_insert_id()")
    customer.set_cid(mysql.connection.fetchone())
    cur.close()
    return customer
