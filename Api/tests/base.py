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
        user2 = json.dumps({
            'email': 'testmail@gmail.com',
            'password': 'testpassword',
            'name': 'testname',

        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['token']


class BaseReview(unittest.TestCase):

    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        with app.app_context():
            # Create all tables
            db.create_all()

        user2 = json.dumps({
            'email': 'test2mail@gmail.com',
            'password': 'test2password',
            'name': 'testnamee',

        })
        response2 = self.client.post('/auth/register', data=user2)
        json_repr2 = json.loads(response2.data.decode())
        self.token2 = json_repr2['token']

        user3 = json.dumps({
            'email': 'test3mail@gmail.com',
            'password': 'test2password',
            'name': 'testnameee',

        })
        response3 = self.client.post('/auth/register', data=user3)
        json_repr3 = json.loads(response3.data.decode())
        self.token3 = json_repr3['token']
