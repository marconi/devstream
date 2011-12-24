# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, json
from flaskext.login import current_user, login_required

from devstream.models.utils import as_group
from devstream.extensions import db
from devstream.models import Group, User


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_home():
    return render_template('dashboard.html')


@dashboard.route('/group/', defaults={'group_id': None},
                 methods=['GET', 'POST', 'PUT'])
@dashboard.route('/group/<group_id>')
@login_required
def group_detail(group_id):
    """ View for inserting, updating and retrieving a group
    instance that haven't been added in the collection. """
    if request.method == "POST":  # inserting
        return insert_posted_group(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass
    else:  # fetch the status from database
        pass


@dashboard.route('/groups/', defaults={'group_id': None},
                 methods=['GET', 'POST', 'PUT'])
@dashboard.route('/groups/<group_id>')
@login_required
def groups(group_id):
    """ View for inserting, updating, retrieving a group
    instance that is added in the collection. Also used
    for displaying all groups. """
    if request.method == "POST":  # inserting
        return insert_posted_group(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass

    # fetch the default status items for the stream
    elif request.method == "GET" and not group_id:
        group_list = []
        for group in current_user.groups:
            group_list.append(dict(id=group.id,
                                   name=group.name,
                                   last_activity=group.last_activity(),
                                   user_id=current_user.id,
                                   members=group.get_members_count()))
        return json.dumps(group_list)


def insert_posted_group(owner, status_json):
    """ Converts status json string into status instance,
    saves it in database and returns the complete group in json format. """
    group = json.loads(status_json, object_hook=as_group)
    group.owner = owner
    group.members.append(owner)
    db.session.add(group)
    db.session.commit()

    # return back the newly saved group with complete
    # attributes so the js model will be updated.
    return json.dumps(dict(id=group.id,
                           name=group.name,
                           last_activity=group.last_activity(),
                           user_id=group.owner.id,
                           members=group.get_members_count()))
