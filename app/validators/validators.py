from app import mongo
from flask import (flash, request, jsonify, Blueprint)
from werkzeug.security import check_password_hash
from app.models.group import Group
from app.models.user import User
import re
import urllib


# Blueprint
validators = Blueprint("validators", __name__)

# variables
pwd_pattern = (
  r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@\-?~$%*^()~+=._])"
  r"(?=\S+$).{8,32}$")
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
        check_value = "false"
    return check_value


@validators.route('/check_email_exists', methods=['GET', 'POST'])
def check_email_exists():
    """
    Read data form ajax call
    Check for existing email
    Return json answer match or no match
    """
    resp = request.form.to_dict(flat=False)
    email = resp["email"][0].lower()
    existing_email = User.check_existing_user(email)
    if existing_email:
        message = "match"
    else:
        message = "no match"
    return jsonify(message)


@validators.route('/check_password/<email>/<check>', methods=['GET', 'POST'])
def check_password(email, check):
    """
    Read data form ajax call
    Check password hash string
    Return json answer match or no match
    """
    user = mongo.db.users.find_one({"email": email})
    if check_password_hash(user["password"], check):
        message = "match"
    else:
        message = "no match"
    return jsonify(message)


def check_img_url(url):
    # https://stackoverflow.com/questions/12474406/python-how-to-get-the-content-type-of-an-url/36882727
    # https://stackoverflow.com/questions/29537298/python-3-urllib-request-urlopen
    """
    Check if string is null, check is false
    Check if url contains http, if not check is false
    If url contains http make urrlib request to open url and read headers
    Get content main type
    If content maintype is image check value is true, else false
    Return check value
    """
    if not url or url is None:
        check_value = True
        return check_value

    if url and "http" not in url:
        check_value = False
        return check_value

    # https://medium.com/@speedforcerun/python-crawler-http-error-403-forbidden-1623ae9ba0f
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

    req = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        check_value = False
    except urllib.error.URLError:
        check_value = False
    else:
        info = response.info()
        if response.getcode() != 200:
            check_value = False
        else:
            if info.get_content_maintype() == "image":
                check_value = True
            else:
                check_value = False
        return check_value


# check if group name is unique
@validators.route("/check_name", methods=['GET', 'POST'])
def check_name():
    """
    Read data form ajax call
    Check if string is not null
    Check if string return objects from MongoDB
    Return response
    """
    resp = request.form.to_dict(flat=False)
    group_name = resp["group_name"][0].lower()
    existing = resp["existing"][0]
    if existing != "none":
        if existing.lower() != group_name:
            match = Group.find_group_by_name(group_name)
            if match:
                check = 'match'
            else:
                check = 'no match'
        else:
            check = 'no match'
    else:
        match = Group.find_group_by_name(group_name)
        if match:
            check = 'match'
        else:
            check = 'no match'
    return jsonify(check)
