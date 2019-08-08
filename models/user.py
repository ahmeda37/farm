from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from main import login,mysql
class User(UserMixin):
	def User(self,username,password):
		self.username = username
		self.password_hash = generate_password_hash(password)

	def set_username(self,username):
		self.username = username

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM users where id="+id+"")
	mysql.connection.commit()
	myresult = cur.fetchone()
	cur.close()
	return myresult

def get_user(username):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * from users where username ='"+username+"'")
	mysql.connection.commit()
	myresult= cur.fetchone()
	cur.close()
	return myresult

def add_user(User):
	cur = mysql.connection.cursor()
	cur.execute("INSERT into users (username,password_hash) Values ('"+User.username+"', '"+User.password_hash+"')")
	mysql.connection.commit()
	myresult = cur.fetchone()
	cur.close()
	return myresult