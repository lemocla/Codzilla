from flask import (flash, render_template, redirect,
                   request, url_for, Blueprint)
from app.models.group import Group
from app.models.event import Event
from app.models.user import User


# Blueprint
groups = Blueprint("groups", __name__)


@groups.route("/group/<group_id>")
def group(group_id):
    group = Group.find_one_group(group_id)
    events = list(Event.find_events_by_id(group["events"]))
    users = list(User.find_users_by_id(group["group_members"]))
    return render_template("group.html", group=group, events=events,
                           users=users)
