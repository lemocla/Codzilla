import os
from flask import render_template, session
from app import create_app
from app.models.user import User
from app.models.notifications import Notification
from datetime import datetime


app = create_app()


# Frequently asked question page
# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
# https://flask.palletsprojects.com/en/2.0.x/errorhandling/
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def new_notifications():
    if "email" in session:
        user = User.check_existing_user(session["email"].lower())
        notifications = list(Notification.get_notifications_for_user(
                         user["_id"]))
        read = list(Notification.get_read_notification(user["_id"]))
        new = len(notifications) - len(read)

        return dict(new=str(new))
    else:
        return dict(new="")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
