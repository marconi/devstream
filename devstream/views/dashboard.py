# -*- coding: utf-8 -*-

import os
import logging
import gevent
from gevent import monkey
from flask import (Blueprint, render_template, request, json, redirect, url_for,
                   flash)
from flaskext.mail import Message
from flaskext.login import current_user, login_required
from flaskext.babel import gettext as _

from devstream.models.utils import as_group
from devstream.extensions import db, mail
from devstream.models import Group, User, InvitationKey
from devstream.libs.roster import get_online_users
from devstream import settings


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(os.path.basename(__file__))
dashboard = Blueprint('dashboard', __name__)
monkey.patch_all()

@dashboard.route('/dashboard')
@login_required
def dashboard_home():
    return render_template('dashboard.html')


@dashboard.route('/group/',
                 defaults={'group_id': None},
                 methods=['GET', 'POST', 'PUT'])
@dashboard.route('/group/<int:group_id>')
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

        # retrieve online users for this group
        online_users = get_online_users(group_id)

        # since this view is being called prior to adding this
        # user to the list of online users, it doesn't include
        # this current user, so we add it manually.
        online_users.add(current_user)

        log.debug(online_users)

        context = {'group': group, 'online_users': online_users}
        return render_template('group_detail.html', **context)


@dashboard.route('/invite',
                 defaults={'invite_key': None},
                 methods=['GET', 'POST'])
@dashboard.route('/invite/<invite_key>')
@login_required
def group_invite(invite_key):
    if invite_key:
        return "%s" % invite_key
    else:
        emails = set([email for email in request.form['invites'].split('&')])
        group_id = int(request.form['group_id'])
        group = Group.query.get_or_404(group_id)

        mail_context = {'site_name': settings.SITE_NAME,
                        'domain_name': settings.SITE_DOMAIN_NAME}

        for email in emails:
            is_registered = False
            user = User.query.filter_by(email=email).first()
            if user:
                is_registered = True

                # if registered, check if the email provided
                # is already a member, if it is just move to next email.
                if user in group.members:
                    log.debug("Ignoring email %s, already a member" % email)
                    continue

            # if email is not yet registered,
            # generate an invite key.
            if not is_registered:
                mail_context['invite_key'] = '1234'

                # we also need to keep a record of invitation for
                # non-registered users so we can take action once user follows
                # the link.
                invite_key = InvitationKey(email, group)
                db.session.add(invite_key)
                db.session.commit()

                mail_context['invite_key'] = invite_key.key

            log.debug("Sending email to: %s" % email)
            # send a message to each email
            mail_context['group'] = group
            mail_context['is_registered'] = is_registered

            subject = render_template('mails/groups/invite_subject.txt',
                                      **mail_context)
            msg = Message(subject=subject, recipients=[email])
            msg.body = render_template('mails/groups/invite.txt', **mail_context)
            gevent.spawn(mail.send, msg)

        return json.dumps(dict())


@dashboard.route('/groups/', defaults={'group_id': None},
                 methods=['GET', 'POST', 'PUT'])
@dashboard.route('/groups/<int:group_id>')
@login_required
def groups(group_id):
    """ View for inserting, updating, retrieving a group
    instance that is added in the collection. Also used
    for displaying all groups. """
    if request.method == "POST":  # inserting
        return insert_posted_group(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass

    # fetch the all the current user's groups
    elif request.method == "GET" and not group_id:
        group_list = []
        for group in current_user.groups:
            group_list.append(dict(id=group.id,
                                   owner_id=group.owner_id,
                                   name=group.name,
                                   last_activity=group.last_activity(),
                                   user_id=current_user.id,
                                   members=len(group.members)))
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
