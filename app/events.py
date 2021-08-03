from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint,
                   jsonify)
from app.models.group import Group
from app.models.event import Event
from app.models.user import User

# Blueprint
events = Blueprint("events", __name__)
