# -*- coding: utf-8 -*-

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.exc import IntegrityError
from flask import render_template, request, session, flash, redirect, url_for
from flaskext.mail import Message

from devstream import app, mail
from devstream.models import User
from devstream.forms.generic import RegistrationForm
from devstream.libs.database import db_session


manager = BCRYPTPasswordManager()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hashed_password = manager.encode(registration_form.password.data)
        new_user = User(email=registration_form.email.data,
                        password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        # send verification email
        # TODO: this should be read from a template
        msg = Message("DevStream Registration",
                      recipients=[new_user.email])
        msg.body = "Click here to verify your registration."
        mail.send(msg)

        flash("Please check your email to verify your registration",
              category="success")
        return redirect(url_for('register'))
    context = {'registration_form': registration_form}
    return render_template('register.html', **context)
