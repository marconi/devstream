# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, json, session
from flaskext.jsonify import jsonify

from devstream import app
from devstream.models.utils import as_status
from devstream.models import User, Status
from devstream.extensions import db
from devstream import settings


status = Blueprint('status', __name__)

@status.route('/status/',
           defaults={'status_id': None}, methods=['GET', 'POST', 'PUT'])
@status.route('/status/<status_id>')
def status_detail(status_id):
    """ View for inserting, updating and retrieving a status
    instance that haven't been added in the collection. """
    current_user = User.query.get(1)
    if request.method == "POST":  # inserting
        return insert_posted_status(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass
    else:  # fetch the status from database
        pass


@status.route('/stream/',
           defaults={'status_id': None},  methods=['GET', 'POST', 'PUT'])
@status.route('/stream/<status_id>')
def stream(status_id):
    """ View for inserting, updating, retrieving a status
    instance that is added in the collection. Also used
    for displaying the default status items on the stream. """
    current_user = User.query.get(1)
    if request.method == "POST":  # inserting
        return insert_posted_status(current_user, request.data)
    elif request.method == "PUT":  # updating
        pass

    # fetch the default status items for the stream
    elif request.method == "GET" and not status_id:
        statuses = Status.query.filter(Status.user_id == current_user.id)
        statuses = statuses.order_by(Status.created.desc())
        statuses = statuses.limit(settings.DEFAULT_STREAM_ITEMS)
        status_list = []
        for status in statuses:
            created = status.created.strftime("%b %d %Y %I:%M %p")
            status_list.append(dict(id=status.id,
                                    status=status.status,
                                    type=status.type,
                                    created=created,
                                    username=status.user.username,
                                    user_id=status.user_id))
        return json.dumps(status_list)

    # fetch a status from the database
    elif request.method == "GET" and status_id:
        pass


@status.route('/stream/more')
@jsonify
def more():
    current_user = User.query.get(1)
    last_id = int(request.args.get('last_id', 0))

    statuses = Status.query.filter(Status.user_id == current_user.id)
    statuses = Status.query.filter(Status.id < last_id)
    statuses = statuses.order_by(Status.created.desc())
    statuses = statuses.limit(settings.DEFAULT_SHOW_MORE_ITEMS)

    status_list = []
    for status in statuses:
        created = status.created.strftime("%b %d %Y %I:%M %p")
        status_list.append(dict(id=status.id,
                                status=status.status,
                                type=status.type,
                                created=created,
                                username=status.user.username,
                                user_id=status.user_id))
    return status_list or None


def insert_posted_status(owner, status_json):
    """ Converts status json string into status instance,
    saves it in database and returns the complete status in json format. """
    status = json.loads(status_json, object_hook=as_status)
    status.user = owner
    db.session.add(status)
    db.session.commit()

    # return back the newly saved status with complete
    # attributes so the js model will be updated.
    created = status.created.strftime("%b %d %Y %I:%M %p")
    return json.dumps(dict(id=status.id,
                           status=status.status,
                           type=status.type,
                           created=created,
                           username=status.user.username,
                           user_id=status.user_id))
