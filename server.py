import json
from flask_pymongo import PyMongo
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'


@app.route('/check-username', methods=["GET"])
def check_username():
    if request.method == "GET":
        username = request.args.get("username")
        result = mongo.db.users.find({"username": username})
        for _ in result:
            return json.dumps({"exist": True})
        return json.dumps({"exist": False})


@app.route('/check-email', methods=["GET"])
def check_email():
    if request.method == "GET":
        email = request.args.get("email")
        result = mongo.db.users.find({"email": email})
        for _ in result:
            return json.dumps({"exist": True})
        return json.dumps({"exist": False})


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form["name"] 
        username = request.form["username"] 
        email = request.form["email"]
        print(name)
        print(username)
        print(email)
        mongo.db.users.insert_one({
            "name": name, 
            "username": username, 
            "email": email, 
            "bio": "", 
            "profileImage": "", 
            "coverImage": ""
        })
        return {"registered": True}
    return {"registered": False}


if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/worldcon"

    mongo = PyMongo(app)

    app.run(host="0.0.0.0", port=5100)
