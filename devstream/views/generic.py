# -*- coding: utf-8 -*-

from flask import render_template
from flaskext.jsonify import jsonify

from devstream import app


@app.route('/')
def home():
    return render_template('home.html', greetings='Hello World!')


@app.route('/stream/more')
@jsonify
def home():
    return [{"author": "Donec placerat",
             "created": "23 Oct 2011",
             "status": "Donec placerat. Nullam nibh dolor, blandit sed.",
             "type": "status"
            },
            {"author": "Sed tempor",
             "created": "23 Oct 2011",
             "status": "imperdiet sit amet, neque. Nam mollis ultrices justo.",
             "type": "git"
            },
            {"author": "Sed vitae tellus",
             "created": "23 Oct 2011",
             "status": "Etiam sem arcu, eleifend sit amet, gravida eget.",
             "type": "status"
            }]
