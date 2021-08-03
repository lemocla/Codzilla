from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint,
                   jsonify)
from app.models.event import Event


# Blueprint
events = Blueprint("events", __name__)


@events.route("/event/<event_id>")
def event(event_id):
    event = Event.find_one_event(event_id)
    return render_template("event.html", event=event)
