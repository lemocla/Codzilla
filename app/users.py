from . import mongo
from flask import (flash, render_template, redirect,
                   request, session, url_for, jsonify, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app.validators import validators

# Blueprint
users = Blueprint("users", __name__)


# Profile
@users.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Get session's user email from MongoDB
    if user in session, display profile page
    """
    user = mongo.db.users.find_one({"email": session["email"].lower()})
    if user:
        return render_template("profile.html", user=user)


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

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        personal_info = {"$set": {
                        "user_imgUrl": request.form.get("user-img"),
                        "first_name": request.form.get("fname"),
                        "last_name": request.form.get("lname"),
                        "city": request.form.get("city"),
                        "country": request.form.get("country"),
                        }}
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      personal_info)
            flash("Your profile has been updated!")
            return redirect(url_for("users.profile", user=user))
        except Exception as e:
            print(e)
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

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.form.get("email") == request.form.get("confirm-email"):
            email_update = {"$set": {"email": request.form.get("email")}}
            try:
                mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                          email_update)
                flash("Your email has been updated successfully")
                session["email"] = request.form.get("email")
                return redirect(url_for("users.profile", user=user))
            except Exception as e:
                print(e)
        else:
            flash("Make sure that new email and confirm email are the same.")
            return render_template("profile.html", user=user)


# Check if password is correct on user input when changing password
@users.route('/check_password/<email>/<check>', methods=['GET', 'POST'])
def check_password(email, check):
    user = mongo.db.users.find_one({"email": email})
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
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
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

        password_update = {"$set": {"password": generate_password_hash(
                           request.form.get("password"))}}
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      password_update)
            flash("Your password has been updated successfully")
            return redirect(url_for("users.profile", user=user))
        except Exception as e:
            print(e)
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
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return render_template("auth.login.html")

    if request.method == "POST":
        preferences = {"$set": {"preferences":
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
                                 "new_follower")}
                                }}
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)}, preferences)
            flash("Your preferences have been updated!")
            return redirect(url_for("users.profile", user=user))
        except Exception as e:
            print(e)
    return render_template("profile.html", user=user)


@users.route("/delete_account/<user_id>")
def delete_account(user_id):
    """
    Remove user email for session cookie
    Delete user from MongoDB
    Redirect to sign up page
    """
    session.pop("email", None)
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    flash("Account successfully deleted")
    return redirect(url_for("auth.signup"))
