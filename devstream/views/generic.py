# -*- coding: utf-8 -*-

from flask import render_template, request, json, session
from flaskext.jsonify import jsonify

from devstream import app
from devstream.libs.database import db_session
from devstream.models.utils import as_status
from devstream.models import User


@app.route('/')
def home():
    return render_template('home.html', greetings='Hello World!')


@app.route('/stream/', defaults={'status_id': None}, methods=['GET', 'POST'])
@app.route('/stream/<status_id>')
def stream(status_id):
    current_user = User.query.get(1)
    if request.method == "POST":  # inserting
        # build the status posted and save to db
        status = json.loads(request.data, object_hook=as_status)
        status.user = current_user
        db_session.add(status)
        db_session.commit()

        # return back the newly saved status with complete
        # attributes so the js model will be updated.
        created = status.created.strftime("%b %d %Y %I:%M %p")
        return json.dumps(dict(id=status.id,
                               status=status.status,
                               type=status.type,
                               created=created,
                               user_id=status.user_id))
    elif request.method == "PUT":  # updating
        print request.form
    return status_id or 'here'


@app.route('/stream/more')
@jsonify
def more():
    data = [{"id": 4,
      "author": "Donec placerat",
      "created": "23 Oct 2011",
      "status": "Donec placerat. Nullam nibh dolor, blandit sed.",
      "type": "status"
    },
    {"id": 3,
      "author": "Donec placerat",
      "created": "23 Oct 2011",
      "status": "Donec placerat. Nullam nibh dolor, blandit sed.",
      "type": "status"
    },
    {"id": 2,
     "author": "Sed tempor",
     "created": "22 Oct 2011",
     "status": "imperdiet sit amet, neque. Nam mollis ultrices justo.",
     "type": "git"
    },
    {"id": 1,
     "author": "Sed vitae tellus",
     "created": "21 Oct 2011",
     "status": "Etiam sem arcu, eleifend sit amet, gravida eget.",
     "type": "git"
    }]

    num = int(request.args.get('num', 1))
    last_id = int(request.args.get('last_id', 0))

    next_index = None
    for index, item in enumerate(data):
        if item['id'] == last_id:
            next_index = index + 1
            break

    if next_index:
        streams = data[next_index:next_index + num]
        return streams or None

    return None
