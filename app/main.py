import os
from . import mail
from flask import (flash, render_template, redirect,
                   session, request, url_for, Blueprint)
# flask mail
from flask_mail import Message
from app.models.event import Event
from app.models.group import Group
from app.models.user import User


# Blueprint
main = Blueprint("main", __name__)


# Search
@main.route("/search", methods=["GET", "POST"])
def search():
    """
    Render template for all groups and events according to
    search query
    Pass variables so that relevant group and event action are
    displayed
    """
    if session:
        user = User.check_existing_user(session["email"])
    else:
        user = None
    query = request.form.get("search")
    events = list(Event.search_events(query))
    groups = list(Group.search_groups(query))
    users = User.find_all_users()

    if user:
        events_attending = list(user["events_attending"])
        events_interest = list(user["events_interest"])
        events_organised = list(user["events_organised"])
        followed = list(user["group_following"])
        owned = list(user["group_owned"])
    else:
        events_attending = []
        events_interest = []
        events_organised = []
        owned = []
        followed = []

    return render_template("browse-events-groups.html",
                           events=events, groups=groups,
                           query=query, user=user,
                           users=users, events_attending=events_attending,
                           events_interest=events_interest,
                           events_organised=events_organised,
                           owned=owned, followed=followed, search=True)


# Homepage
@main.route("/")
@main.route("/home")
def home():
    """
    Render template for homepage
    Fetch the latest 6 coming events
    If user in session, pass variables so that the relevant actions for
    events are displayed
    """
    # Variables
    events = Event.upcoming_events()
    total = len(Event.find_all_active_events())
    users = User.find_all_users()
    if session.get("email"):
        user = User.check_existing_user(session["email"].lower())
    else:
        user = None
    if user:
        events_attending = list(user["events_attending"])
        events_interest = list(user["events_interest"])
        events_organised = list(user["events_organised"])
    else:
        events_attending = []
        events_interest = []
        events_organised = []
    return render_template("home.html", events=events, users=users,
                           total=total, user=user,
                           events_attending=events_attending,
                           events_interest=events_interest,
                           events_organised=events_organised)


# All events and groups
@main.route("/browse_events_groups/")
def browse_events_groups():
    """
    Render template for all groups and events
    Find all active and current events
    If user in session, pass the variables so that
    relevant user actions for groups and events are displayed
    """
    events = Event.find_all_active_events()
    groups = Group.find_all_groups()
    users = User.find_all_users()

    if session.get("email"):
        user = User.check_existing_user(session["email"].lower())
    else:
        user = None

    if user:
        events_attending = list(user["events_attending"])
        events_interest = list(user["events_interest"])
        events_organised = list(user["events_organised"])
        followed = list(user["group_following"])
        owned = list(user["group_owned"])
    else:
        events_attending = []
        events_interest = []
        events_organised = []
        owned = []
        followed = []
    return render_template("browse-events-groups.html", events=events,
                           groups=groups, users=users, user=user,
                           events_attending=events_attending,
                           events_interest=events_interest,
                           events_organised=events_organised,
                           owned=owned, followed=followed)


""""
https://sendgrid.com/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid/
"""


@main.route("/contact_us", methods=['GET', 'POST'])
def contact_us():
    """
    Get input from user in contact form
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
        return redirect(url_for('main.contact_us'))
    return render_template("contact_us.html")


# Accessibility page
@main.route("/accessibility")
def accessibility():
    """
    Return template for accessibility page
    """
    return render_template("accessibility.html")


# Frequently asked question page
@main.route("/faq")
def faq():
    """
    Return template for Frequently Asked Question
    """
    return render_template("faq.html")


# Privacy page
@main.route("/privacy")
def privacy():
    """
    Return template for privacy page
    """
    return render_template('privacy.html')
