from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
from dbconnect import get_user_by_id,login,submitproduct,create_db_table,insert_user
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

if __name__ == "__main__":
    #app.debug = True
    app.run(debug=True)
    # app.run() #run app