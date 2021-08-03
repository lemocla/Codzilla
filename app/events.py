from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint,
                   jsonify)
from bson.objectid import ObjectId
from app import mongo
from app.models.event import Event
from app.models.user import User

# Blueprint
events = Blueprint("events", __name__)


@events.route("/event/<event_id>")
def event(event_id):
    event = Event.find_one_event(event_id)
    owner = User.find_user_by_id(event["created_by"])
    attendees = list(User.find_users_by_id(event["attendees"]))
    questions_answers = list(mongo.db.questions_answers.find(
                             {"event_id": ObjectId(event_id)}))
    if owner:
        admin = True
    else:
        admin = False
    return render_template("event.html", event=event,
                           admin=admin, owner=owner,
                           attendees=attendees,
                           questions_answers=questions_answers)
