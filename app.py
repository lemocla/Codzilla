import os
from flask import render_template
from app import create_app

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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
