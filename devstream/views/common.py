# -*- coding: utf-8 -*-

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.exc import IntegrityError
from flask import (Blueprint, render_template, request, session, flash,
                   redirect, url_for)
from flaskext.mail import Message
from flaskext.babel import gettext as _
from flaskext.login import login_user, logout_user, login_required

from devstream.extensions import mail, db, login_manager
from devstream.models import User, ActivationKey
from devstream.forms.generic import RegistrationForm, LoginForm
from devstream import settings


common = Blueprint('common', __name__)
manager = BCRYPTPasswordManager()

@common.route('/')
def home():
    return render_template('home.html')


@common.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hashed_password = manager.encode(registration_form.password.data)
        new_user = User(email=registration_form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # create activation key
        activation_key = ActivationKey(new_user)
        db.session.add(activation_key)
        db.session.commit()

        # send verification email
        mail_context = {'site_name': settings.SITE_NAME,
                        'domain_name': settings.SITE_DOMAIN_NAME,
                        'activation_key': activation_key.key,
                        'expiration_days': settings.ACTIVATION_EXPIRATION}
        subject = render_template('mails/registration/activation_subject.txt',
                                  **mail_context)
        msg = Message(subject=subject, recipients=[new_user.email])
        msg.body = render_template('mails/registration/activation.txt',
                                   **mail_context)
        mail.send(msg)

        flash(_("Please check your email to verify your registration."),
              category="success")
        return redirect(url_for('common.register'))
    context = {'registration_form': registration_form}
    return render_template('register.html', **context)


@common.route('/activate/<activation_key>', methods=['GET'])
def activate(activation_key):
    activation = ActivationKey.query.filter_by(key=activation_key,
                                               is_activated=False).first()
    if activation and not activation.is_expired():
        activation.is_activated = True
        activation.user.is_activated = True
        db.session.commit()
        flash(_("Your account has been activated, you can now login."),
              category="success")
    else:
        msg = "The activation link is invalid or has expired, " \
              "click here to request for new activation."
        flash(_(msg), category="error")
    return redirect(url_for('common.home'))


@common.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        login_user(login_form.user)
    else:
        msg = "It's either your email or password is incorrect."
        flash(_(msg), category="error")
    return redirect(url_for('dashboard.dashboard_home'))


@common.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('common.home'))
