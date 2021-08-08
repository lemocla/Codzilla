from flask import (flash, render_template, redirect,
                   request, session, url_for, jsonify, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from app.validators import validators
# Classes
from app.models.user import User
from app.models.group import Group
from app.models.event import Event

# Blueprint
users = Blueprint("users", __name__)


# Profile
@users.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Get session's user email from MongoDB
    if user in session, display profile page
    """
    user = User.check_existing_user(session["email"].lower())
    if user:
        return render_template("profile.html", user=user)
    else:
        return render_template("login.html")


# Edit personal information
@users.route('/edit_info/<user_id>', methods=['GET', 'POST'])
def edit_info(user_id):
    """
    Get user and user email from MongoDB
    Build dictionary from user input to update personal info
    Update user document on MongoDB
    Flash message to inform user of successful update
    Redirect to profile page
    """

    user = User.find_user_by_id(user_id)

    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        pers_info = {"user_imgUrl": request.form.get("user-img"),
                     "first_name": request.form.get("fname"),
                     "last_name": request.form.get("lname"),
                     "city": request.form.get("city"),
                     "country": request.form.get("country")}

        User.edit_user(user_id, pers_info)
        flash("Your profile has been updated!")
        return redirect(url_for("users.profile", user=user))

    return render_template("profile.html", user=user)


# Edit email
@users.route('/edit_email/<user_id>', methods=['GET', 'POST'])
def edit_email(user_id):
    """
    Get user and user email from MongoDB
    Check both new and confirm email are the same
    If so, build dictionary from user input
    If not, flash message to inform user
    Update user document on MongoDB
    Flash message to inform user of successful update
    Redirect to profile page
    """

    user = User.find_user_by_id(user_id)

    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":

        if request.form.get("email") == request.form.get("confirm-email"):

            User.edit_user(user_id, request.form.get("email"))
            flash("Your email has been updated successfully")
            session["email"] = request.form.get("email")

            return redirect(url_for("users.profile", user=user))

        else:
            flash("Make sure that new email and confirm email are the same.")
            return render_template("profile.html", user=user)


# Check if password is correct on user input when changing password
@users.route('/check_password/<email>/<check>', methods=['GET', 'POST'])
def check_password(email, check):
    user = User.check_existing_user(email.lower())

    if check_password_hash(user["password"], check):
        message = "match"
    else:
        message = "no match"
    return jsonify(message)


# Edit password
@users.route('/edit_password/<user_id>', methods=['GET', 'POST'])
def edit_password(user_id):
    """
    Get user from MongoDB
    Check both new and confirm passwords are the same
    Check if the password matches the one on MongoDB
    Check if the password pass the regex pattern
    If not, flash message to inform user
    If so, build dictionary from user input
    Update user document on MongoDB
    Flash message to inform user of successful update
    Redirect to profile page
    """
    user = User.find_user_by_id(user_id)
    if not user:
        return render_template("users.login.html")

    if request.method == "POST":

        # Check if both new and confirmation input are the same
        if request.form.get("password") != request.form.get("conf-new-pwd"):
            flash("Make sure that both passwords matches")
            return render_template("profile.html", user=user)

        # Check if current password matches the one on MongoDB
        if not check_password_hash(user["password"],
                                   request.form.get("current-pwd")):
            flash("Current password is incorrect")
            return render_template("profile.html", user=user)

        if not validators.check_regex(validators.pwd_pattern,
                                      request.form.get("password"),
                                      "password"):
            flash("Password format is not valid, please inclue a mix of "
                  "letters, numbers and symbols.")
            return render_template("profile.html", user=user)

        password_update = {"password": generate_password_hash(
                           request.form.get("password"))}

        User.edit_user(user_id, password_update)
        flash("Your password has been updated successfully")
        return redirect(url_for("users.profile", user=user))

    return render_template("profile.html", user=user)


# Edit preferences
@users.route('/edit_preferences/<user_id>', methods=['GET', 'POST'])
def edit_preferences(user_id):
    """
    Get user and user email from MongoDB
    Build dictionary from user input
    Update user document on MongoDB
    Flash message to inform user of successful update
    Redirect to profile page
    """
    user = User.find_user_by_id(user_id)

    if not user:
        return render_template("auth.login.html")

    if request.method == "POST":
        preferences = {"preferences":
                       {"event_reminder": request.form.get(
                         "event_reminder"),
                        "query_answered": request.form.get(
                         "query_answered"),
                        "event_update": request.form.get(
                         "event_update"),
                        "new_participant": request.form.get(
                         "new_participant"),
                        "event_question": request.form.get(
                         "event_question"),
                        "new_follower": request.form.get(
                         "new_follower")}}

        User.edit_user(user_id, preferences)
        flash("Your preferences have been updated!")
        return redirect(url_for("users.profile", user=user))

    return render_template("profile.html", user=user)


@users.route("/delete_account/<user_id>")
def delete_account(user_id):
    """
    Remove user email for session cookie
    Delete user from MongoDB
    Redirect to sign up page
    """
    session.pop("email", None)
    User.delete_one_user(user_id)
    flash("Account successfully deleted")
    return redirect(url_for("auth.signup"))


@users.route("/my_groups")
def my_groups():
    user = User.check_existing_user(session["email"].lower())
    if not user:
        return redirect(url_for("login"))

    groups_owned = list(Group.find_groups_by_id(user["group_owned"]))
    groups_following = list(Group.find_groups_by_id(user["group_following"]))
    return render_template("my-groups.html", user=user,
                           groups_owned=groups_owned,
                           groups_following=groups_following)


@users.route("/my_events")
def my_events():
    user = User.check_existing_user(session["email"].lower())
    if not user:
        return redirect(url_for("login"))

    organising = list(Event.find_events_by_id(user["events_organised"]))
    attending = list(Event.find_events_by_id(user["events_attending"]))
    interesting = list(Event.find_events_by_id(user["events_interest"]))
    return render_template("my-events.html", user=user,
                           organising=organising,
                           attending=attending,
                           interesting=interesting)


@users.route("/attend", methods=['GET', 'POST'])
def attend():
    # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
    resp = request.form.to_dict(flat=False)
    user_id = resp["user_id"][0]
    event_id = resp["event_id"][0]
    user = User.find_user_by_id(user_id)
    if user:
        User.append_list(user_id, "events_attending", event_id)
        Event.add_to_list(event_id, "attendees", user_id)
        message = "success"
    return jsonify(message)
