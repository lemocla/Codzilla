import os
from . import mongo
from . import mail
from flask import (flash, render_template, redirect,
                   request, url_for, Blueprint)
# flask mail
from flask_mail import Message
from datetime import datetime

# Blueprint
main = Blueprint("main", __name__)


# Homepage
@main.route("/")
@main.route("/Home")
def home():
    # Variables
    events = list(mongo.db.events.find(
                  {"date_start": {"$gte": datetime.today()}}).sort(
                  "date_start", 1))
    users = mongo.db.users.find()
    return render_template("home.html", events=events, users=users)


@main.route("/browse_events_groups/")
def browse_events_groups():
    # Variables
    events = list(mongo.db.events.find(
                  {"date_start": {"$gte": datetime.today()}}).sort(
                  "date_start", 1))
    groups = list(mongo.db.groups.find())
    users = mongo.db.users.find()
    return render_template("browse-events-groups.html", events=events,
                           groups=groups, users=users)


""""
https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/
"""


@main.route("/contact_us", methods=['GET', 'POST'])
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
@main.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")


# Frequently asked question page
@main.route("/faq")
def faq():
    return render_template("faq.html")
