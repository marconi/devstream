# -*- coding: utf-8 -*-

from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, EqualTo


class RegistrationForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', [
        Required(), EqualTo('confirm', message="Password doesn't match.")])
    confirm = PasswordField('Confirm Password')
