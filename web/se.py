from flask import *

app = Flask(__name__)

@app.route("/main")
def mainpage():
    from db import queries
    influencer = queries.main_influencer()
    brand = queries.main_brand()
    ## influencer, brand = jsonify(influencer, brand)

    return render_template("index.html", influencer = influencer, brand = brand) 
    

@app.route('/channel/<chname>') 
def channel(chname):
    return 'Hello, %s'%(chname)    


app.run(debug=True, port=5000)