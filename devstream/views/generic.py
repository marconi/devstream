# -*- coding: utf-8 -*-

from flask import render_template, request
from flaskext.jsonify import jsonify

from devstream import app


@app.route('/')
def home():
    return render_template('home.html', greetings='Hello World!')


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
     "type": "status"
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
