from flask import *
from db import login_mysql
mydb, cursor = login_mysql.login()

app = Flask(__name__)

@app.route("/main")
def mainpage():
    from db import mains
    influencer = mains.main_influencer()
    brand = mains.main_brand()
    ##influencer, brand = jsonify(influencer, brand)

    return render_template("main.html", influencer = influencer, brand = brand) 

@app.route('/channel/<chname>') 
def channel(chname):
    return 'Hello, %s'%(chname)    


@app.route('/hed')
def hello_pybo():
    from db import queries
    brand = queries.main_brand()
    return render_template("test.html",brand = brand) 


@app.route('/brand')
def brandbrief():
    from db import brief_brand
    brand_sub = brief_brand.brief_sub()
    brand_view = brief_brand.brief_view()
    brand_video = brief_brand.brief_video()

    return render_template("brand.html", sub = brand_sub, view = brand_view, video = brand_video)


@app.route('/influencer')
def influbrief():
    from db import brief_influencer
    influ_sub = brief_influencer.brief_sub()
    influ_view = brief_influencer.brief_view()
    influ_video = brief_influencer.brief_video()

    return render_template("influencer.html", sub = influ_sub, view = influ_view, video = influ_video) 
    
app.run(debug=True, port=5000)

