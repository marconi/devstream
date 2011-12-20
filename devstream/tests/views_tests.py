# -*- coding: utf-8 -*-

import re
from flaskext.testing import TestCase
from flask import Flask, request
from flaskext.babel import Babel
from flaskext.mail import Mail

from devstream.extensions import db, mail
from devstream import create_app
from devstream import settings
from devstream.models import User
from devstream.forms.generic import RegistrationForm
from devstream.views.common import register


class GenericViewsTests(TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        app = create_app()
        db_uri = "%s/%s" % (settings.DATABASE_URI_PREFIX,
                            settings.TEST_DATABASE_NAME)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['TESTING'] = True

        settings.SITE_DOMAIN_NAME = 'localhost:5000'
        return app

    def test_registration(self):
        response = self.client.get('/register')
        self.assertStatus(response, 200)
        self.assertTrue(self.get_context_variable('registration_form'))
    
    def test_registration_empty(self):
        response = self.client.post('/register', data={})
        self.assertEqual(response.data.count('This field is required.'), 2)
    
    def test_registration_mismatch_password(self):
        response = self.client.post('/register', data={'password': 'admin',
                                                       'confirm': 'random'})
        self.assertTrue("Password doesn&#39;t match." in response.data)
    
    def test_registration_taken_email(self):
        db.session.add(User(email='foo@bar.com', password='admin'))
        db.session.commit()
        response = self.client.post('/register', data={'email': 'foo@bar.com',
                                                       'password': 'admin',
                                                       'confirm': 'admin'})
        self.assertTrue("Email is already taken." in response.data)

    def test_registration_success(self):
        response = self.client.get('/register')
        registration_form = self.get_context_variable('registration_form')
        csrf_token = registration_form.csrf.data

        with mail.record_messages() as outbox:
            response = self.client.post('/register',
                                        data={'email': 'foo@bar.com',
                                              'password': 'admin',
                                              'confirm': 'admin',
                                              'csrf': csrf_token},
                                        follow_redirects=True)
            msg = "Please check your email to verify your registration."
            self.assertTrue(msg in response.data)
            self.assertEqual(len(outbox), 1)

            # check that we have one unverified user
            self.assertEqual(User.query.filter_by(is_active=False).count(), 1)

            # extract the verification url
            match = re.findall(r'(http://.+)', outbox[0].body)
            self.assertTrue(match)

            # requests doesn't accept domain, so replace it with empty string.
            domain = settings.SITE_DOMAIN_NAME
            verification_url = match[0].replace("http://%s" % domain, "")

            response = self.client.get(verification_url, follow_redirects=True)
            msg = "Your account has been activated, you can now login."
            self.assertTrue(msg in response.data)

            # check that we have now one active user
            self.assertEqual(User.query.filter_by(is_active=True).count(), 1)


if __name__ == '__main__':
    unittest.main()
