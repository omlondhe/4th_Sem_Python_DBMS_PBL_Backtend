from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.route('/create')
def create_collection():
    try:
        print(mongo.db.create_collection("test"))
    except Exception as e:
        print(e)
    return 'done'

if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/worldcon"

    mongo = PyMongo(app)

    app.run(host="0.0.0.0", port=5100)
