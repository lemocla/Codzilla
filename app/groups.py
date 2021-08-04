from flask import (flash, render_template, redirect,
                   request, url_for, session, Blueprint,
                   jsonify)
from app.models.group import Group
from app.models.event import Event
from app.models.user import User

# Blueprint
groups = Blueprint("groups", __name__)


@groups.route("/group/<group_id>")
def group(group_id):
    group = Group.find_one_group(group_id)
    events = list(Event.find_events_by_id(group["events"]))
    users = list(User.find_users_by_id(group["group_members"]))

    admins = list(User.find_users_by_id(group["group_admin"]))
    if session:
        for a in admins:
            if session["email"] == a["email"]:
                admin = True
            else:
                admin = False
    else:
        admin = False
    return render_template("group.html", group=group, events=events,
                           users=users, admin=admin)


@groups.route("/add_group", methods=["GET", "POST"])
def add_group():
    if not session["email"]:
        return redirect(url_for('login'))
    user = User.check_existing_user(session["email"])
    new_group = Group(group_name=request.form.get("group_name"),
                      group_city=request.form.get("group_city"),
                      group_country=request.form.get("group_country"),
                      group_description=request.form.get("group_description"),
                      img_url=request.form.get("img_url"),
                      group_admin=[user["_id"]])
    if request.method == "POST":
        new = new_group.insert_into_database()
        print(new)
        User.append_list(user["_id"], "group_owned", new.inserted_id)
        flash("Group successfully added!")
        return redirect(url_for('users.my_groups'))
    return render_template("add_group.html", user=user)


@groups.route("/edit_group/<group_id>", methods=["GET", "POST"])
def edit_group(group_id):

    if not session["email"]:
        return redirect(url_for('login'))

    user = User.check_existing_user(session["email"])
    group = Group.find_one_group(group_id)

    if request.method == "POST":
        edit_info = {"group_name": request.form.get("group_name"),
                     "group_city": request.form.get("group_city"),
                     "group_country": request.form.get("group_country"),
                     "group_description": request.form.get(
                                          "group_description"),
                     "img_url": request.form.get("img_url")}
        Group.update_group(group_id, edit_info)
        flash("Group successfully edited!")
        return redirect(url_for('users.my_groups'))

    return render_template("edit_group.html", user=user, group=group,
                           group_id=group_id)


# delete group modals
@groups.route('/delete-group-modal/<group_id>', methods=['GET', 'POST'])
def delete_group_modal(group_id):
    group = Group.find_one_group(group_id)
    message = group["group_name"]
    return jsonify(message)


# delete group modals
@groups.route('/delete-group/<group_id>', methods=['GET', 'POST'])
def delete_group(group_id):
    Group.delete_one_group(group_id)
    flash("Your group has been successfully deleted")
    return redirect(url_for('users.my_groups'))
