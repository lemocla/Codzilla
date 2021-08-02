from flask import (flash, render_template, redirect,
                   request, url_for, Blueprint)
from app.models.group import Group


# Blueprint
groups = Blueprint("groups", __name__)


@groups.route("/group/<group_id>")
def group(group_id):
    group = Group.find_one_group(group_id)
    return render_template("group.html", group=group)
