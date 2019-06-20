import unittest

from ..api import db
from run import app
from config import application_config


class BaseUser(unittest.TestCase):

    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
