import unittest

from flask import json

from ..api import db
from run import app
from config import application_config


class BaseUser(unittest.TestCase):

    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        with app.app_context():
            db.create_all()


class BaseCategory(unittest.TestCase):

    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        with app.app_context():
            # Create all tables
            db.create_all()

        user = json.dumps({
            'email': 'testmail@gmail.com',
            'password': 'testpassword',
            'name': 'testname',

        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['token']
