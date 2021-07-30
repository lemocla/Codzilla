import os
from . import mongo
from . import mail
from flask import (flash, render_template, redirect,
                   request, session, url_for, jsonify, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
# flask mail
from flask_mail import Message
import re
import jwt
from time import time


# Blueprint
routes = Blueprint("routes", __name__)

# variables
pwd_pattern = "^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@\-?~$%*^()~+=._])(?=\S+$).{8,32}$"
name_pattern = ("^[a-zA-Z._-]{1,20}$")


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


# Home page
@routes.route("/")
@routes.route("/home")
def home():
    return render_template("home.html")


# Sign up functionality
@routes.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("signup"))

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
                return redirect(url_for("complete_profile",
                                        email=session["email"]))
            except Exception as e:
                print(e)
        else:
            return redirect(url_for("signup"))

    return render_template("signup.html")


# Complete profile functionality
# https://testdriven.io/blog/flask-sessions/
@routes.route("/complete_profile/<email>", methods=["GET", "POST"])
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
            return redirect(url_for("profile_completed",
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


@routes.route("/profile_completed/<email>")
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
@routes.route("/login", methods=["GET", "POST"])
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
                return redirect(url_for("profile_completed",
                                email=session["email"]))
            else:
                flash("Incorrect password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect email and/or password")
            return redirect(url_for("login"))
    return render_template("login.html")


# Log out
@routes.route("/logout")
def logout():
    """
    Remove user from session cookies
    Flash message to inform user
    Redirect to login page
    """
    session.pop("email", None)
    flash("You have been logged out")
    return redirect(url_for("login"))


# Profile
@routes.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Get session's user email from MongoDB
    if user in session, display profile page
    """
    user = mongo.db.users.find_one({"email": session["email"].lower()})
    if user:
        return render_template("profile.html", user=user)


# Edit personal information
@routes.route('/edit_info/<user_id>', methods=['GET', 'POST'])
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
            return redirect(url_for("profile", user=user))
        except Exception as e:
            print(e)
        return render_template("profile.html", user=user)


# Edit email
@routes.route('/edit_email/<user_id>', methods=['GET', 'POST'])
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
                return redirect(url_for("profile", user=user))
            except Exception as e:
                print(e)
        else:
            flash("Make sure that new email and confirm email are the same.")
            return render_template("profile.html", user=user)


# Check if password is correct on user input when changing password
@routes.route('/check_password/<email>/<check>', methods=['GET', 'POST'])
def check_password(email, check):
    user = mongo.db.users.find_one({"email": email})
    if check_password_hash(user["password"], check):
        message = "match"
    else:
        message = "no match"
    return jsonify(message)


# Edit password
@routes.route('/edit_password/<user_id>', methods=['GET', 'POST'])
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
        return render_template("login.html")

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

        if not check_regex(pwd_pattern,
                           request.form.get("password"), "password"):
            flash("Password format is not valid, please inclue a mix of "
                  "letters, numbers and symbols.")
            return render_template("profile.html", user=user)

        password_update = {"$set": {"password": generate_password_hash(
                           request.form.get("password"))}}
        try:
            mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                      password_update)
            flash("Your password has been updated successfully")
            return redirect(url_for("profile", user=user))
        except Exception as e:
            print(e)
    return render_template("profile.html", user=user)


# Edit preferences
@routes.route('/edit_preferences/<user_id>', methods=['GET', 'POST'])
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
        return render_template("login.html")

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
            return redirect(url_for("profile", user=user))
        except Exception as e:
            print(e)
    return render_template("profile.html", user=user)


@routes.route("/delete_account/<user_id>")
def delete_account(user_id):
    """
    Remove user email for session cookie
    Delete user from MongoDB
    Redirect to sign up page
    """
    session.pop("email", None)
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    flash("Account successfully deleted")
    return redirect(url_for("signup"))


@routes.route("/get_events")
def get_events():
    events = mongo.db.events.find()
    return render_template("allevents.html", events=events)


""""
https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/
"""


@routes.route("/contact_us", methods=['GET', 'POST'])
def contact_us():
    """ Get input from user in contact form
    Send a acknowledgment email to suer
    Send email with email, fullname and message to the website owner
    Lets user know the email has been sent
    """
    if request.method == 'POST':
        sender_fullname = request.form['fullname']
        sender_email = request.form['email']
        sender_message = request.form['message']
        admin_email = os.environ.get('MAIL_DEFAULT_SENDER')
        recipients = [sender_email, admin_email]
        # flask documentation https://pythonhosted.org/Flask-Mail/
        with mail.connect() as conn:
            for recipient in recipients:
                if recipient == admin_email:
                    message = (f"<h3>Hello</h3>"
                               "<p>Please find below message from:</p>"
                               f"<p><b>Name:</b> {sender_fullname}</p> "
                               f"<p><b>Email:</b> {sender_email}</p> "
                               f"<p><b>Message:</b> {sender_message} </p>")
                    subject = f"New query from: {sender_fullname}"

                elif recipient == sender_email:
                    message = (f"<h3>Hello {sender_fullname},</h3>"
                               "<p>We have received your message and aim"
                               " to respond within the next 2 working "
                               "days.</p>"
                               "<p>Best regards</p>"
                               "<p>Codzilla Team</p>"
                               )
                    subject = 'Thank your for your query'

                msg = Message(recipients=[recipient],
                              html=message,
                              subject=subject)
                conn.send(msg)

        flash("Your message was sent successfully!")
        return redirect(url_for('contact_us'))
    return render_template("contact_us.html")


def get_reset_token(email, expires=500):
    """
    Return a token to encode user email
    """
    return jwt.encode({'user': email,
                       'exp':    time() + expires},
                      key=os.environ.get("SECRET_KEY"))


@routes.route("/password_reset_request", methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
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
        return redirect(url_for('login'))
    return render_template("login.html")


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


@routes.route("/reset-password/<token>", methods=['GET', 'POST'])
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
        return redirect(url_for('login'))

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
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return
    return render_template("reset-password.html")


# Accessibility page
@routes.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")


# Frequently asked question page
@routes.route("/faq")
def faq():
    return render_template("faq.html")


# Frequently asked question page
# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@routes.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@routes.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
