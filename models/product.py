from main import mysql

class Product():
	def Product(self,name):
		self.name = name
	def get_name(self):
		return self.name

def getProducts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    mysql.connection.commit()
    myresult = cur.fetchall()
    cur.close()
    return myresult
def addProduct(product):
    cur = mysql.connection.cursor()
    cur.execute("INSERT into products (name) VALUES ('"+product.name+"')")
    mysql.connection.commit()
    myresult = cur.fetchone()
    cur.close()
    return myresult