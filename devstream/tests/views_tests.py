# -*- coding: utf-8 -*-

from flaskext.testing import TestCase
from flask import Flask
from flaskext.babel import Babel
from flaskext.mail import Mail

from devstream import create_app



class GenericViewsTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_app(self):
        return create_app()

    def test_registration(self):
        response = self.client.get('/register')
        print response
        self.assert_status(response, 200)


if __name__ == '__main__':
    unittest.main()
