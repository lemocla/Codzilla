import os
from flask import (Flask, render_template, request, redirect, url_for, flash, session)
# connect Flask to MongoDB
from flask_pymongo import PyMongo
# flask mail
from flask_mail import Mail, Message
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
import re


# import environment
if os.path.exists("env.py"):
    import env


# create an instance of flask
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# email
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# create an instance of PyMongo
mongo = PyMongo(app)


# Create an instance of mail
mail = Mail(app)


# variables
pwd_pattern = "^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@\-?~$%*^()~+=._])(?=\S+$).{8,32}$"
name_pattern = ("^[a-zA-Z._-]{1,20}$")


def check_regex(pattern, data, string_flash):
    check = re.search(pattern, data)
    if check:
        match = True
    else:
        match = False
        flash(f"Your {string_flash} is invalid!")
    print(match)
    return bool(match)


def signup_validation(password, fname, lname):
    check_pwd = check_regex(pwd_pattern, password, "password")
    check_fname = check_regex(name_pattern, fname, "first name")
    check_lname = check_regex(name_pattern, lname, "last name")
    check_list = [check_pwd, check_fname, check_lname]
    return check_list


def check_box(value):
    if value == "on":
        check_value = True
    else:
        check_value = False
    return check_value


# Sign up
@app.route("/")
def base():
    return render_template("base.html", page_title="base template")


# Sign up functionality
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Username already exists, please sign in")
            return redirect(url_for("signup"))
        # form validation
        password = request.form.get("password")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        valid = all(signup_validation(password, fname, lname))
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
                return redirect(url_for("complete_profile", email=session["email"]))
            except Exception as e:
                print(e)
        else:
            return redirect(url_for("signup"))

    return render_template("signup.html", page_title="sign-up page")


# Complete profile functionality
# https://testdriven.io/blog/flask-sessions/
@app.route("/complete_profile/<email>", methods=["GET", "POST"])
def complete_profile(email):
    # Get the session's user mail from MongoDB
    email = mongo.db.users.find_one({"email": session["email"].lower()})["email"]
    # Get the first name for session user from MongoDB
    fname = mongo.db.users.find_one({"email": session["email"].lower()})["first_name"].capitalize()
    # Get ID from mongoDB
    user_id = mongo.db.users.find_one({"email": session["email"].lower()})["_id"]

    # Complete user profile
    if request.method == "POST":
        profile = {"$set": {
            "user_imgUrl": request.form.get("user-img"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "preferences": {"event_reminder": check_box(request.form.get("event_reminder")),
                            "query_answered": check_box(request.form.get("query_answered")),
                            "event_update": check_box(request.form.get("event_update")),
                            "new_participant": check_box(request.form.get("new_participant")),
                            "event_question": check_box(request.form.get("event_question")),
                            "new_follower": check_box(request.form.get("new_follower"))},
            "profile_completed": True
        }}
        try:
            mongo.db.users.update({"_id": ObjectId(user_id)}, profile)
            flash("Profile successfully completed")
            return redirect(url_for("profile_completed", email=session["email"]))
        except Exception as e:
            print(e)
    if session["email"]:
        return render_template(
            "complete-profile.html",
            page_title="complete profile page",
            email=email,
            name=fname)


@app.route("/profile_completed/<email>")
def profile_completed(email):
    # Get the session's user mail from MongoDB
    email = mongo.db.users.find_one(
            {"email": session["email"].lower()})["email"]
    # Get the first name for session user from MongoDB
    fname = mongo.db.users.find_one(
            {"email": session["email"].lower()})["first_name"].capitalize()    

    if session["email"]:
        return render_template(
            "profile-completed.html",
            page_title="profile completed",
            email=email, name=fname)


@app.route("/get_events")
def get_events():
    events = mongo.db.events.find()
    return render_template("allevents.html", events=events)


""""
https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/
"""


@app.route("/contact_us", methods=['GET', 'POST'])
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
                               " to respond within the next 2 working days.</p>"
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
    return render_template("contact_us.html", page_title="contact us")


@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html",
                           page_title="accessibility statement")


@app.route("/faq")
def faq():
    return render_template("faq.html", page_title="frequently asked question")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
