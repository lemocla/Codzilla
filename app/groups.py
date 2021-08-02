from flask import (flash, render_template, redirect,
                   request, url_for, Blueprint)
from app.models.group import Group
from app.models.event import Event


# Blueprint
groups = Blueprint("groups", __name__)


@groups.route("/group/<group_id>")
def group(group_id):
    group = Group.find_one_group(group_id)
    events = list(Event.find_events_by_id(group["events"]))
    return render_template("group.html", group=group, events=events)
