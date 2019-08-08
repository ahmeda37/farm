from main import mysql

class Sale_order():
	def Sale_order(self,total,customer, item):
		self.total = total
		self.customer = customer
		self.item = item
	def add_item(self,item):
		if self.item:
			self.item.append(item)
		else:
			self.item = [item]
	def add_total(self,total):
		self.total = self.total + total
	def get_total(self):
		return self.total
	def get_items(self):
		return self.item