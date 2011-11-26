# -*- coding: utf-8 -*-

from flask import render_template
from devstream import app


@app.route('/')
def home():
    return render_template('home.html', greetings='Hello World!')
