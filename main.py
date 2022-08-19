# from crypt import methods
from itertools import product
from urllib.parse import _NetlocResultMixinStr
from flask import Flask, render_template, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
from dbconnect import get_user_by_id,login,submitproduct,create_db_table,insert_user,daily_transaction,qrscanner
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# @app.route("/db", methods=['GET'])
# def create_db():
#     create_db_table()

@app.route('/api/user/login', methods=['POST'])
def api_login():
    user_data = request.get_json()
    return jsonify(login(user_data))

@app.route('/api/users/add',  methods = ['POST'])
def api_add_user1():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/product/add',  methods = ['POST'])
def api_add_user():
    product = request.get_json()
    return jsonify(submitproduct(product))

@app.route('/report', methods=["GET"])
def report():
    daily_report = daily_transaction()
    return render_template("report.html",rows = daily_report)

@app.route('/scan', methods=["GET"])
def qrscan():
    item_code =  qrscanner()
    return render_template("createorder.html",code = item_code)

@app.route('/createorder', methods=["GET","POST"])
def createorder():
    if request.method == "GET":
        return render_template("createorder.html")
    else:
        qty = request.form['qty']
        code= request.form["itemcode"]
        product = {"user_id":1,"barcode":code,"qty":qty}
        submitproduct(product)
        return render_template("createorder.html")

if __name__ == "__main__":
    #app.debug = True
    app.run(debug=True)
    # app.run() #run app