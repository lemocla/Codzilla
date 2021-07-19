import os
from flask import (Flask, render_template)
# connect Flask to MongoDB
from flask_pymongo import PyMongo
# for later: from bson.objectid import ObjectId

# import environment
if os.path.exists("env.py"):
    import env

# create an instance of flask
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


# create an instance of PyMongo
mongo = PyMongo(app)


# test function to make sure app is properly configured
@app.route("/")
@app.route("/get_events")
def get_events():
    events = mongo.db.events.find()
    return render_template("all_events.html", events=events)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
