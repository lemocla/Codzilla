from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint)
from bson.objectid import ObjectId
from app import mongo
from datetime import datetime
from app.models.event import Event
from app.models.user import User
from app.models.group import Group
from app.models.questions_answers import Question
from app.validators import validators
from app.models.notifications import Notification


# Blueprint
events = Blueprint("events", __name__)


@events.route("/event/<event_id>")
def event(event_id):
    event = Event.find_one_event(event_id)
    owner = User.find_user_by_id(event["created_by"])
    attendees = list(User.find_users_by_id(event["attendees"]))
    questions_answers = Question.find_all_questions_answers(event_id)
    if session:
        user = User.check_existing_user(session["email"].lower())
        if owner["_id"] == user["_id"]:
            admin = True
        else:
            admin = False
    else:
        user = None
        admin = False

    return render_template("event.html", event=event,
                           admin=admin, owner=owner,
                           attendees=attendees,
                           questions_answers=questions_answers,
                           user=user)


# https://koenwoortman.com/python-flask-multiple-routes-for-one-function/
@events.route("/add-event/<group_id>)", methods=["GET", "POST"])
@events.route("/add-event)", methods=["GET", "POST"])
def add_event(group_id=None):

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

        if validators.check_box(request.form.get("is_endtime")) == "true":
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

        User.append_list(user["_id"], "events_organised", new.inserted_id)
        flash("Event successfully added!")

        if group_id:
            Group.add_to_list(group_id, "events", new.inserted_id)
            return redirect(url_for('groups.group', group_id=group_id))
        else:
            if request.form.get('group') is not None:
                gp = Group.find_group_by_name(request.form.get('group'))
                Group.add_to_list(gp["_id"], "events", new.inserted_id)
            return redirect(url_for('users.my_events'))

    if (group_id):
        group = Group.find_one_group(group_id)
        return render_template("add-event.html", user=user,
                               types=types, categories=categories,
                               groups=groups, group=group)
    else:
        group = None
        return render_template("add-event.html", user=user,
                               types=types, categories=categories,
                               groups=groups)


@events.route("/edit-event/<event_id>/<group_id>)", methods=["GET", "POST"])
@events.route("/edit-event/<event_id>)", methods=["GET", "POST"])
def edit_event(event_id, group_id=None):

    user = User.check_existing_user(session["email"])
    types = mongo.db.types.find()
    categories = mongo.db.categories.find()
    groups = list(Group.find_groups_by_id(user["group_owned"]))
    event = Event.find_one_event(event_id)
    event_status = mongo.db.event_status.find()

    if not session["email"]:
        return redirect(url_for('login'))

    if request.method == "POST":
        # date time to ISO format
        start_string = (f'{request.form.get("date_start")}T'
                        f'{request.form.get("time_start")}:00')

        if validators.check_box(request.form.get("is_endtime")) == "true":
            end_string = (f'{request.form.get("date_start")}T'
                          f'{request.form.get("time_end")}:00')
        else:
            end_string = start_string

        date_start = datetime.strptime(start_string, '%d/%m/%YT%H:%M:%S')
        date_end = datetime.strptime(end_string, '%d/%m/%YT%H:%M:%S')

        current_group = event["group"]
        print(f"current_group {current_group}")
        print(f"value from request {request.form.get('group')}")

        if request.form.get('group') != current_group:
            # Remove from event from list of events in group
            if group_id:
                print(f"origin from group and there's a group id {group_id}")
                Group.remove_from_list(group_id, "events", event_id)
            else:
                if current_group:
                    gp_id = Group.find_group_by_name(current_group)["_id"]
                    print(f"look for the group because not from group id {gp_id}")
                    Group.remove_from_list(gp_id, "events", event_id)
            # Add to new group if any
            if request.form.get('group'):
                new_gp = Group.find_group_by_name(
                         request.form.get('group'))["_id"]
                print(f"should add to new group {new_gp}")
                group_id = new_gp
                Group.add_to_list(new_gp, "events", event_id)
            else:
                group_id = None

        # Notifications
        send_to = []
        for attendee in event["attendees"]:
            att = User.find_user_by_id(attendee)
            if att["preferences"]["event_update"] == "true":
                send_to.append(ObjectId(att["_id"]))

            if date_start != event["date_start"]:
                print("date has changed - notification")
                notification = Notification.set_col_update(
                               send_to, event_id, "date", date_start)

                Notification.insert_notification(notification)

            if(request.form.get("event_location") != event[
               "event_location"]):
                print("location has changed - notification")
                notification = Notification.set_col_update(
                               send_to, event_id, "location",
                               request.form.get("event_location"))
                Notification.insert_notification(notification)

        update = {"event_title": request.form.get("event_title"),
                  "event_type": request.form.get("event_type"),
                  "event_category": request.form.get("event_category"),
                  "group": request.form.get("group"),
                  "date_start": date_start,
                  "is_endtime": validators.check_box(request.form.get(
                                "is_endtime")),
                  "date_end": date_end,
                  "event_description": request.form.get("event_description"),
                  "event_location": request.form.get("event_location"),
                  "event_link": request.form.get("event_link"),
                  "img_url": request.form.get("img_url"),
                  "max_attendees": request.form.get("max_attendees"),
                  "status": request.form.get("status")}

        Event.update_event(event_id, update)
        flash("Event successfully edited!")

        if group_id:
            return redirect(url_for('groups.group', group_id=group_id))
        else:
            return redirect(url_for('users.my_events'))

    if (group_id):
        group = Group.find_one_group(group_id)
        return render_template("edit-event.html", user=user,
                               types=types, categories=categories,
                               groups=groups, event_status=event_status,
                               group=group, event_id=event_id, event=event)
    else:
        group = None
        return render_template("edit-event.html", user=user,
                               types=types, categories=categories,
                               event_status=event_status, groups=groups,
                               event_id=event_id, event=event)


@events.route("/cancel-event/<event_id>)", methods=["GET", "POST"])
def cancel_event(event_id):

    if not session["email"]:
        return redirect(url_for('login'))

    if request.method == "POST":
        # Notifications
        send_to = []
        event = Event.find_one_event(event_id)
        for attendee in event["attendees"]:
            att = User.find_user_by_id(attendee)
            if att["preferences"]["event_update"] == "true":
                send_to.append(ObjectId(att["_id"]))

        print("event cancelled - notification")
        notification = Notification.set_col_cancellation(
                               send_to, event_id)
        Notification.insert_notification(notification)

        status = {"status": "cancelled"}
        Event.update_event(event_id, status)
        flash("Event succesfully cancelled!")
        return redirect(url_for('events.event',
                        event_id=event_id))


@events.route("/delete-event/<event_id>)", methods=["GET", "POST"])
def delete_event(event_id):

    if not session["email"]:
        return redirect(url_for('login'))

    event = Event.find_one_event(event_id)
    user = User.check_existing_user(session["email"])
    if request.method == "POST":
        # remove from group if any - events
        if event["group"]:
            group = Group.find_group_by_name(event["group"])
            Group.remove_from_list(group["_id"], "events", event_id)
        # remove from users - events_organised
        if event["created_by"] == user["_id"]:
            User.remove_from_list(user["_id"], "events_organised", event_id)
        # remove from users - events_attendees
        if len(list(event["attendees"])) > 0:
            for attendee in list(event["attendees"]):
                User.remove_from_list(attendee, "events_attending", event_id)
        # remove from db - events_interest
        users_interested = list(User.find_users_by_array_element(
                                "events_interest", event_id))

        if len(users_interested) > 0:
            for user_int in users_interested:
                User.remove_from_list(user_int["_id"], "events_interest",
                                      event_id)
        Event.delete_event(event_id)
        flash("Event succesfully deleted!")
        return redirect(url_for('users.my_events'))


@events.route("/add_question/<event_id>)", methods=["GET", "POST"])
def add_question(event_id):
    if not session:
        return redirect(url_for('login'))

    user = User.check_existing_user(session["email"])

    if request.method == "POST":
        question = Question(question=request.form.get("question"),
                            asked_by=user["_id"],
                            event_id=ObjectId(event_id),
                            answered=False)

        # notification
        event = Event.find_one_event(event_id)
        event_admin = User.find_user_by_id(event["created_by"])

        if event_admin["preferences"]["event_question"] == "true":
            notification = Notification.set_col_question(
                            user["_id"], event_id, event_admin["_id"])
            Notification.insert_notification(notification)

        question.insert_into_database()
        return redirect(url_for('events.event', event_id=event_id))


@events.route("/edit_question/<event_id>/<qa_id>)", methods=["GET", "POST"])
def edit_question(event_id, qa_id):
    if not session:
        return redirect(url_for('login'))

    if request.method == "POST":
        question = {"question": request.form.get("question")}
        Question.update_qa(qa_id, question)

        return redirect(url_for('events.event', event_id=event_id))


@events.route("/delete_question/<event_id>/<qa_id>)", methods=["GET", "POST"])
def delete_question(event_id, qa_id):
    if not session:
        return redirect(url_for('login'))

    question = Question.find_one_qa(qa_id)
    if request.method == "POST":
        if question["answered"] is True:
            print("update the question to none")
            update = {"question": None}
            Question.update_qa(qa_id, update)
        else:
            print("no answers so can delete")
            Question.delete_one_question(qa_id)
        return redirect(url_for('events.event', event_id=event_id))


@events.route("/answer_question/<event_id>/<qa_id>)", methods=["GET", "POST"])
def answer_question(event_id, qa_id):
    if not session:
        return redirect(url_for('login'))
    event = Event.find_one_event(event_id)

    if request.method == "POST":
        answer = {"answer": request.form.get("answer"),
                  "answered_by": event["created_by"],
                  "answered": True}

        # notification
        event = Event.find_one_event(event_id)
        qa = Question.find_one_qa(qa_id)
        user = User.find_user_by_id(qa["asked_by"])
        if user["preferences"]["query_answered"] == "true":
            notification = Notification.set_col_answer(
                           user["_id"], event["_id"])
            Notification.insert_notification(notification)

        Question.update_qa(qa_id, answer)

        return redirect(url_for('events.event', event_id=event_id))


@events.route("/edit_answer/<event_id>/<qa_id>)", methods=["GET", "POST"])
def edit_answer(event_id, qa_id):
    if not session:
        return redirect(url_for('login'))

    if request.method == "POST":
        answer = {"answer": request.form.get("answer")}
        Question.update_qa(qa_id, answer)

        return redirect(url_for('events.event', event_id=event_id))


@events.route("/delete_answer/<event_id>/<qa_id>)", methods=["GET", "POST"])
def delete_answer(event_id, qa_id):
    if not session:
        return redirect(url_for('login'))

    question = Question.find_one_qa(qa_id)
    if request.method == "POST":
        if question["question"] is not None:
            update = {"answer": None, "answered": False}
            Question.update_qa(qa_id, update)
        elif question["question"] is None:
            print("no answers so can delete")
            Question.delete_one_question(qa_id)
        return redirect(url_for('events.event', event_id=event_id))


@events.context_processor
def new_notifications():
    if session:
        user = User.check_existing_user(session["email"].lower())
        notifications = list(Notification.get_notifications_for_user(
                         user["_id"]))
        read = list(Notification.get_read_notification(user["_id"]))
        new = len(notifications) - len(read)
        print(new)
        return dict(new=str(new))
