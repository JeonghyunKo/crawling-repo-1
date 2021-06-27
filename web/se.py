from flask import *
from db import login_mysql
mydb, cursor = login_mysql.login()

app = Flask(__name__)

@app.route("/main")
def mainpage():
    from db import queries
    influencer = queries.main_influencer()
    brand = queries.main_brand()
    ##influencer, brand = jsonify(influencer, brand)

    return render_template("index.html", influencer = influencer, brand = brand) 
    

@app.route('/channel/<chname>') 
def channel(chname):
    return 'Hello, %s'%(chname)    


@app.route('/hed')
def hello_pybo():
    from db import queries
    brand = queries.main_brand()
    return render_template("test.html",brand = brand) 

app.run(debug=True, port=5000)

