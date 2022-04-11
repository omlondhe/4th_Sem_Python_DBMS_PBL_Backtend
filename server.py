from crypt import methods
import datetime
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
        uid = request.form.get("uid")
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        mongo.db.users.insert_one({
            "uid": uid,
            "name": name, 
            "username": username, 
            "email": email, 
            "bio": "", 
            "profileImage": "", 
            "coverImage": ""
        })
        return {"registered": True}
    return {"registered": False}


@app.route("/get-user-data", methods=["GET"])
def getUserData():
    if request.method == "GET":
        uid = request.args.get("uid")
        cursor = mongo.db.users.find({"uid": uid})
        result = {}
        for data in cursor:
            result["id"] = str(data["_id"])
            result["uid"] = data["uid"]
            result["name"] = data["name"]
            result["username"] = data["username"]
            result["email"] = data["email"]
            result["bio"] = data["bio"]
            result["profileImage"] = data["profileImage"]
            result["coverImage"] = data["coverImage"]
        return json.dumps(result)
    return json.dumps({"status": "failure"})


@app.route("/add-post", methods=["POST"])
def addPost():
    if request.method == "POST":
        imageURL = request.form.get("imageURL")
        caption = request.form.get("caption")
        by = request.form.get("by")
        mongo.db.posts.insert_one({
            "imageURL": imageURL,
            "caption": caption, 
            "by": by, 
            "at": datetime.datetime.utcnow(),
            "likes": [],
        })
        return {"added": True}
    return {"added": False}


@app.route("/get-posts", methods=["GET"])
def getPosts():
    if request.method == "GET":
        skip = request.args.get("skip")
        cursor = mongo.db.posts.find().sort(key_or_list="at", direction=-1).skip(int(skip)).limit(10)
        results = []
        result = {}
        
        for data in cursor:
            result["imageURL"] = data["imageURL"]
            result["caption"] = data["caption"] 
            result["by"] = data["by"] 
            result["at"] = str(data["at"])
            result["likes"] = data["likes"]
            results.append(result)
        
        return json.dumps(results)
    return json.dumps({"status": "failure"})


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        uid = request.form.get("uid")
        name = request.form.get("name")
        username = request.form.get("username")
        bio = request.form.get("bio")
        mongo.db.users.update_one(
            {"uid": uid}, 
            {
                "$set": {
                    "name": name, 
                    "username": username, 
                    "bio": bio, 
                }
            })
        return {"updated": True}
    return {"updated": False}


@app.route("/remove-profile-image", methods=["POST"])
def removeProfileImage():
    if request.method == "POST":
        uid = request.form.get("uid")
        mongo.db.users.update_one(
            {"uid": uid},
            {
                "$set": {
                    "profileImage": ""
                }
            }
        )
        return {"removed": True}
    return {"removed": False}


@app.route("/remove-cover-image", methods=["POST"])
def removeCoverImage():
    if request.method == "POST":
        uid = request.form.get("uid")
        mongo.db.users.update_one(
            {"uid": uid},
            {
                "$set": {
                    "coverImage": ""
                }
            }
        )
        return {"removed": True}
    return {"removed": False}


@app.route("/update-profile-image", methods=["POST"])
def updateProfileImage():
    if request.method == "POST":
        uid = request.form.get("uid")
        profileImage = request.form.get("profileImage")
        mongo.db.users.update_one(
            {"uid": uid},
            {
                "$set": {
                    "profileImage": profileImage
                }
            }
        )
        return {"updated": True}
    return {"updated": False}


@app.route("/update-cover-image", methods=["POST"])
def updateCoverImage():
    if request.method == "POST":
        uid = request.form.get("uid")
        coverImage = request.form.get("coverImage")
        mongo.db.users.update_one(
            {"uid": uid},
            {
                "$set": {
                    "coverImage": coverImage
                }
            }
        )
        return {"updated": True}
    return {"updated": False}


@app.route("/get-users", methods=["GET"])
def getUsers():
    if request.method == "GET":
        searchString = request.args.get("searchString")
        cursor = mongo.db.users.find({
            "$or": [
                {"name": { "$regex": searchString }},
                {"username": { "$regex": searchString }} 
            ]
        })
        results = []
        result = {}
        
        for data in cursor:
            result["name"] = data["name"]
            result["username"] = data["username"] 
            result["uid"] = data["uid"] 
            result["profileImage"] = data["profileImage"]
            results.append(result)
        
        return json.dumps(results)
    return json.dumps({"status": "failure"})


if __name__ == '__main__':
    app.config["MONGO_URI"] = "mongodb://localhost:27017/worldcon"

    mongo = PyMongo(app)

    app.run(host="0.0.0.0", port=5100, debug=True)
