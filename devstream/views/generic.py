# -*- coding: utf-8 -*-

from flask import render_template, request, session

from devstream import app
from devstream.forms.generic import RegistrationForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        pass
    else:
        pass
    context = {'registration_form': registration_form}
    return render_template('register.html', **context)
