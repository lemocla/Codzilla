from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint,
                   jsonify)
from bson.objectid import ObjectId
from app import mongo
from datetime import datetime
from app.models.event import Event
from app.models.user import User
from app.models.group import Group
from app.validators import validators

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


@events.route("/add-event", methods=["GET", "POST"])
def add_event():
    user = User.check_existing_user(session["email"])
    types = mongo.db.types.find()
    categories = mongo.db.categories.find()
    groups = list(Group.find_groups_by_id(user["group_owned"]))

    if not session["email"]:
        return redirect(url_for('login'))

    if request.method == "POST":
        # https://stackoverflow.com/questions/4460698/python-convert-string-representation-of-date-to-iso-8601
        start_string = (f'{request.form.get("date_start")}T'
                        f'{request.form.get("time_start")}:00')

        if validators.check_box(request.form.get("is_endtime")):
            end_string = (f'{request.form.get("date_start")}T'
                          f'{request.form.get("time_end")}:00')
        else:
            end_string = start_string

        date_start = datetime.strptime(start_string, '%d/%m/%YT%H:%M:%S')
        date_end = datetime.strptime(end_string, '%d/%m/%YT%H:%M:%S')

        new_event = Event(
                      event_title=request.form.get("event_title"),
                      event_type=request.form.get("event_type"),
                      event_category=request.form.get("event_category"),
                      group=request.form.get("group"),
                      date_start=date_start,
                      is_endtime=validators.check_box(request.form.get(
                                 "is_endtime")),
                      date_end=date_end,
                      event_description=request.form.get("event_description"),
                      event_location=request.form.get("event_location"),
                      event_link=request.form.get("event_link"),
                      img_url=request.form.get("img_url"),
                      max_attendees=request.form.get("max_attendees"),
                      status="active",
                      created_by=user["_id"])
        new = new_event.insert_into_database()
        print(new)
        User.append_list(user["_id"], "events_organised", new.inserted_id)
        flash("Event successfully added!")
        return redirect(url_for('users.my_events'))
    return render_template("add-event.html", user=user,
                           types=types, categories=categories,
                           groups=groups)
