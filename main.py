from livereload import Server
from flask import Flask, render_template
import datetime
app = Flask(__name__)


@app.route('/')
def index():
    this_dict ={
        "customer": "First Last",
        "address": "1234 Something Ave, Edmonton",
        "sale_order": "1234",
        "date": datetime.datetime.now()
    }
    return render_template('index.html', this_dict=this_dict)

if __name__ == '__main__':
    app.debug=True
    server = Server(app.wsgi_app)
    server.serve()
    #app.run(debug='True')