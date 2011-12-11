# -*- coding: utf-8 -*-

from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, EqualTo, ValidationError

from devstream.libs.database import db_session
from devstream.models import User


class RegistrationForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', [
        Required(), EqualTo('confirm', message="Password doesn't match.")])
    confirm = PasswordField('Confirm Password')

    def validate_email(form, field):
        """ Validate that email is not yet taken. """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already taken.')
