from app import mongo
from flask import (flash, jsonify, Blueprint)
from werkzeug.security import check_password_hash
import re
import urllib


# Blueprint
validators = Blueprint("validators", __name__)

# variables
pwd_pattern = r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@\-?~$%*^()~+=._])(?=\S+$).{8,32}$"
name_pattern = r"^[a-zA-Z-_. ]{1,32}$"


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


@validators.route('/check_password/<email>/<check>', methods=['GET', 'POST'])
def check_password(email, check):
    user = mongo.db.users.find_one({"email": email})
    if check_password_hash(user["password"], check):
        message = "match"
    else:
        message = "no match"
    return jsonify(message)


def check_img_url(url):
    # https://stackoverflow.com/questions/12474406/python-how-to-get-the-content-type-of-an-url/36882727
    # https://stackoverflow.com/questions/29537298/python-3-urllib-request-urlopen
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        print(e)
        check_value = False
    else:
        info = response.info()
        print(response.getcode())
        print(info.get_content_type())      # -> text/html
        print(info.get_content_maintype())  # -> text
        print(info.get_content_subtype())

        if response.getcode() != 200:
            check_value = False

        else:
            if info.get_content_maintype() == "image":
                check_value = True
            else:
                check_value = False

        return check_value
