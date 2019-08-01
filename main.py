from livereload import Server
from flask import Flask, render_template,request, redirect
import datetime
app = Flask(__name__)
this_dict ={
    "customer": "First Last",
    "address": "1234 Something Ave, Edmonton",
    "sale_order": "1234",
    "date": datetime.datetime.now()
}
items = {
    "1":"Bananas",
    "2":"Limes",
    "3":"Mangos"
}
order={}
count=0
total=0

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
        print(item)
        order.update({count:item})
        print(order)
        count +=1
        total += item['total']
        return render_template('index.html', this_dict=this_dict, items=items, result=order,total=total)
    return render_template('index.html',this_dict=this_dict,items=items, result=order,total=total)

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
    count = 0
    total = 0
    order = {}
    return redirect("/")
if __name__ == '__main__':
    app.debug=True
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(debug='True')