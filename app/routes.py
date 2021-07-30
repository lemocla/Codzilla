import os
from . import mongo
from . import mail
from flask import (flash, render_template, redirect,
                   request, session, url_for, jsonify, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
# flask mail
from flask_mail import Message
# regex
import re

# Blueprint
routes = Blueprint("routes", __name__)


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


# Homepage
# Log in
@routes.route("/")
@routes.route("/Home")
def home():
    return render_template("home.html")


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
