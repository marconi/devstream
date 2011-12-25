# -*- coding: utf-8 -*-

import logging

from flask import (Blueprint, render_template, request, json, redirect, url_for,
                   flash)
from flaskext.login import current_user, login_required
from flaskext.babel import gettext as _

from devstream.models.utils import as_group
from devstream.extensions import db
from devstream.models import Group, User


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def dashboard_home():
    return render_template('dashboard.html')


@dashboard.route('/group/', defaults={'group_id': None},
                 methods=['GET', 'POST', 'PUT'])
@dashboard.route('/group/<group_id>')
@login_required
def group(group_id):
    """ View for inserting, updating and retrieving a group
    instance that haven't been added in the collection. """
    if request.method == "POST":  # inserting
        return insert_posted_group(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass

     # fetch the status from database a.k.a group_detail
    elif request.method == "GET" and group_id:
        group = Group.query.get(group_id)

        # check that current_user is a member or owner of the group.
        # if not, redirect to dashboard and show message.
        if current_user not in group.members:
            msg = _("You don't have enough permission to access that group.")
            flash(_(msg), category="error")
            return redirect(url_for('dashboard.dashboard_home'))

        context = {'group': group}
        return render_template('group_detail.html', **context)


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


@dashboard.route('/groups/leave', methods=['POST'])
@login_required
def groups_leave():
    ids = [int(i) for i in request.form['ids'].split('&')]
    groups = Group.query.filter(Group.id.in_(ids))
    for group in groups:
        # if the current user is the owner,
        # delete the group.
        # TODO: send notification to members that the group has been
        # deleted by the owner.
        if group.owner_id == current_user.id:
            db.session.delete(group)
        else:
            group.members.remove(current_user)
    db.session.commit()
    return json.dumps({'ids': ids})


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
                           owner_id=group.owner.id,
                           members=group.get_members_count()))
