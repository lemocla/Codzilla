import os
from flask import (flash, render_template, redirect,
                   request, url_for, Blueprint)
from app.models.group import Group


# Blueprint
groups = Blueprint("groups", __name__)


@groups.route("/group")
def group():
    return render_template("group.html")
