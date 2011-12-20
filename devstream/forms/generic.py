# -*- coding: utf-8 -*-

from cryptacular.bcrypt import BCRYPTPasswordManager
from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Email, EqualTo, ValidationError

from devstream.models import User


manager = BCRYPTPasswordManager()

class RegistrationForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('confirm', message="Password doesn't match.")])
    confirm = PasswordField('Confirm Password')

    def validate_email(form, field):
        """ Validate that email is not yet taken. """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already taken.')


class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])

    def validate(self):
        self.user = User.query.filter_by(email=self.email.data,
                                         is_activated=True).first()
        if not self.user:
            return False
        return manager.check(self.user.password, self.password.data)
