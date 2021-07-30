import os
from . import mongo
from . import mail
from flask import (flash, render_template, redirect,
                   request, session, url_for, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
# flask mail
from flask_mail import Message
# regext
import re
# encoding / decoding tokens
import jwt
from time import time


# Blueprint
auth = Blueprint("auth", __name__)

# variables
pwd_pattern = r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@\-?~$%*^()~+=._])(?=\S+$).{8,32}$"
name_pattern = r"^[a-zA-Z._-]{1,20}$"


def check_regex(pattern, data, string_flash):
    """
    Check that user input match regex pattern
    Flash message if data invalid
    """
    check = re.search(pattern, data)
    if check:
        match = True
    else:
        match = False
        flash(f"Your {string_flash} is invalid!")
    print(match)
    return bool(match)


def signup_validation(password, fname, lname):
    """
    Check that sign up input against criteria
    """
    check_pwd = check_regex(pwd_pattern, password, "password")
    check_fname = check_regex(name_pattern, fname, "first name")
    check_lname = check_regex(name_pattern, lname, "last name")
    check_list = [check_pwd, check_fname, check_lname]
    return check_list


def check_box(value):
    """
    Set default value for checkbox
    """
    if value == "on":
        check_value = "true"
    else:
        check_value = 'false'
    return check_value


# Sign up functionality
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Check if user email exists,
    If so, add flash message informing user
    Check if data are valid
    Create a signup dictionary from user input
    Insert in MongoBD if data is valid and,
    Add the new user email into 'session' cookie
    Redirect to complete profile page
    """
    if request.method == "POST":
        # check if email already exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        if existing_user:
            flash("Username already exists, please sign in")
            return redirect(url_for("auth.signup"))

        # form validation
        valid = all(signup_validation(request.form.get("password"),
                    request.form.get("fname"), request.form.get("lname")))
        # sign up dictionary
        signup = {
            "first_name": request.form.get("fname").lower(),
            "last_name": request.form.get("lname").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "city": "",
            "country": "",
            "events_attending": [],
            "user_imgUrl": "",
            "events_interest": [],
            "events_organised": [],
            "group_following": [],
            "group_owned": [],
            "notifications_msg": [],
            "preferences": {"event_reminder": True,
                            "query_answered": True,
                            "event_update": True,
                            "new_participant": True,
                            "event_question": True,
                            "new_follower": True},
            "profile_completed": False
        }
        if valid:
            try:
                mongo.db.users.insert_one(signup)
                flash("Sign up successful!")
                session['email'] = request.form['email'].lower()
                return redirect(url_for("auth.complete_profile",
                                        email=session["email"]))
            except Exception as e:
                print(e)
        else:
            return redirect(url_for("auth.signup"))

    return render_template("signup.html")


# Complete profile functionality
# https://testdriven.io/blog/flask-sessions/
@auth.route("/complete_profile/<email>", methods=["GET", "POST"])
def complete_profile(email):
    """
    Get email, first name and user ID from MongoDB
    Build dictionary from user input
    Update user in MongoDB
    Flash message to inform user of successful completion
    Redirect to complete profile completed page
    """
    # Get ID from mongoDB
    user_id = mongo.db.users.find_one({"email":
                                      session["email"].lower()})["_id"]
    # Complete user profile
    if request.method == "POST":
        profile = {"$set": {
            "user_imgUrl": request.form.get("user-img"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "preferences": {"event_reminder": check_box(request.form.get(
                             "event_reminder")),
                            "query_answered": check_box(request.form.get(
                             "query_answered")),
                            "event_update": check_box(request.form.get(
                             "event_update")),
                            "new_participant": check_box(request.form.get(
                             "new_participant")),
                            "event_question": check_box(request.form.get(
                             "event_question")),
                            "new_follower": check_box(request.form.get(
                             "new_follower"))},
            "profile_completed": True
        }}
        try:
            mongo.db.users.update({"_id": ObjectId(user_id)}, profile)
            flash("Profile successfully completed")
            return redirect(url_for("auth.profile_completed",
                                    email=session["email"]))
        except Exception as e:
            print(e)
    if session["email"]:
        # Get the first name for session user from MongoDB
        fname = mongo.db.users.find_one({"email":
                                        session["email"].lower()})[
                                        "first_name"].capitalize()
        return render_template(
            "complete-profile.html", email=email, name=fname)


@auth.route("/profile_completed/<email>")
def profile_completed(email):
    """
    Get email and first name from MongoDB
    Display page if user in session
    """
    email = mongo.db.users.find_one(
            {"email": session["email"].lower()})["email"]
    fname = mongo.db.users.find_one(
            {"email": session["email"].lower()})["first_name"].capitalize()

    if session["email"]:
        return render_template(
            "profile-completed.html", email=email, name=fname)


# Log in
@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Get existing user from MongoDB
    Check if existing user
    If existing user, check password
    If password match redirect to profile completed
    If no password match, redirect to login page and,
    Inform user password is incorrect
    If no existing user, flash message to inform user
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # check if passowrd matches
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                session["email"] = request.form.get("email").lower()
                return redirect(url_for("auth.profile_completed",
                                email=session["email"]))
            else:
                flash("Incorrect password")
                return redirect(url_for("auth.login"))

        else:
            # username doesn't exist
            flash("Incorrect email and/or password")
            return redirect(url_for("auth.login"))
    return render_template("login.html")


# Log out
@auth.route("/logout")
def logout():
    """
    Remove user from session cookies
    Flash message to inform user
    Redirect to login page
    """
    session.pop("email", None)
    flash("You have been logged out")
    return redirect(url_for("auth.login"))


"""
Reset password
https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968
"""


# Get token for reset link
def get_reset_token(email, expires=500):
    """
    Return a token to encode user email
    """
    return jwt.encode({'user': email,
                       'exp':    time() + expires},
                      key=os.environ.get("SECRET_KEY"))


# Request password request
@auth.route("/password_reset_request", methods=['GET', 'POST'])
def password_reset_request():
    """
    Get email for user from user input
    Check if the user exists in MongoDB
    Create token link using get_reset_token
    Render email template (as need template literal for the link)
    Send email to user with link to reset password page
    """
    if request.method == 'POST':
        email = request.form.get('email-request')
        user = mongo.db.users.find_one({"email": email.lower()})
        if not user:
            flash("Your email couldn't be verified")
            return redirect(url_for('auth.login'))
        token = get_reset_token(email)

        # flask documentation https://pythonhosted.org/Flask-Mail/
        message = render_template('reset-email.html',
                                  token=token)
        subject = "Codzilla password reset"
        msg = Message(recipients=[email],
                      html=message,
                      subject=subject)
        mail.send(msg)
        flash("Reset password request successfully sent")
        return redirect(url_for('auth.login'))
    return render_template("login.html")


# Function to verify token
def verify_reset_token(token):
    """
    Decode token and return email
    Check if email exists in MongoDB
    """
    try:
        email = jwt.decode(token, os.environ.get("SECRET_KEY"),
                           algorithms=["HS256"])['user']
    except Exception as e:
        print(e)
        flash("Your link has timed out. Reset your password again"
              " for a new link")
        return
    existing_user = mongo.db.users.find_one({"email": email.lower()})
    return existing_user


# Password reset page
@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    """
    Decode token and return existing user
    If not an exisitng user, redirect to login & inform user
    Render the reset password html page
    Collect information from user input
    Check if both password match and pass regex pattern check
    Update password on MongoDB
    Return to login page
    """
    existing_user = verify_reset_token(token)

    if not existing_user:
        flash("Your password couldn't be reset")
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        password = request.form.get('password')
        confirmation_password = request.form.get('conf-new-pwd')

        if password != confirmation_password:
            flash("Make sure that both passwords match")
            return render_template("reset-password.html")

        if not check_regex(pwd_pattern,
                           request.form.get("password"), "password"):
            flash("Password format is not valid, please inclue a mix of "
                  "letters, numbers and symbols.")
            return render_template("reset-password.html")

        user_id = existing_user["_id"]
        password_update = {"$set": {"password": generate_password_hash(
                            password)}}
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      password_update)
            flash("Your password has been reset successfully!")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            return
    return render_template("reset-password.html")
