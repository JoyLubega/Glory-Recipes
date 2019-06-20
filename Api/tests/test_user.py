from flask import json

from .base import BaseUser
from Api.api import app, db


class UserTestcase(BaseUser):

    def test_success_registration(self):
        """Should register user successfully"""
        user = json.dumps({
            'email': 'test_user@gmail.com',
            'password': 'mypassword',
            'name': 'Joyce',
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', response.data.decode())

    def test_registration_with_no_credentials(self):
        """Should throw error for missing credentials"""
        user = json.dumps({
            'name': '',
            'email': '',
            'password': ''

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Missing', response.data.decode())

    def test_registration_with_name_as_integer(self):
        """Should throw error for name being an integer"""
        user = json.dumps({
            'name': 888,
            'email': 'tw@gmail.com',
            'password': 'mypassword'

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Numbers cant be a Name', response.data.decode())

    def test_registration_with_name_as_space(self):
        """Should throw error for name being a space"""
        user = json.dumps({
            'name': " ",
            'email': 'tw@gmail.com',
            'password': 'mypassword'

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('A space is not a name', response.data.decode())

    def test_registration_with_name_as_symbol(self):
        """Should throw error for name being a symbol"""
        user = json.dumps({
            'name': "$",
            'email': 'tw@gmail.com',
            'password': 'mypassword'

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Name should be in alphabetical', response.data.decode())

    def test_registration_with_invalid_email(self):
        """Should throw error for missing credentials"""
        user = json.dumps({
            'name': 'test',
            'email': 'test.com',
            'password': 'testpassword'

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.data.decode())

    def test_registration_with_invalid_keys(self):
        """Should throw error for missing keys"""
        user = json.dumps({
            'username': 'test',
            'email': 'test.com',
            'password': 'testpassword'

        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Check the keys and try again", response.data.decode())

    def test_registration_with_existing_email(self):
        """Should throw error for missing credentials"""
        user1 = json.dumps({
            'name': 'test',
            'email': 'test@gmail.com',
            'password': 'testpassword'

        })
        self.client.post('/auth/register', data=user1)

        user2 = json.dumps({
            'name': 'test',
            'email': 'test@gmail.com',
            'password': 'testpassword'

        })
        response2 = self.client.post('/auth/register', data=user2)
        self.assertEqual(response2.status_code, 401)
        self.assertIn("Email Already exists", response2.data.decode())

    def test_successful_login(self):
        """Return 201 and a token"""
        self.test_success_registration()
        user = json.dumps({
            'email': 'test_user@gmail.com',
            'password': 'mypassword'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Login Successful', response.data.decode())

    def test_login_invalid_user(self):
        """Return 401, user doesnot exist"""
        self.test_success_registration()
        user = json.dumps({
            'email': 'test@gmail.com',
            'password': 'testpassword'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Incorrect email or password', response.data.decode())

    def test_login_invalid_email(self):
        """Return 401, email is invalid"""
        self.test_success_registration()
        user = json.dumps({
            'email': 'test',
            'password': 'testpassword'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com', response.data.decode()) # noqa E501

    def test_login_with_empty_filelds(self):
        """Return 401, user doesnot exist"""
        self.test_success_registration()
        user = json.dumps({
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing login credentials', response.data.decode())

    def test_login_with_no_filelds(self):
        """Return 401, fields do not exist"""
        self.test_success_registration()
        user = json.dumps({
            'tel': '',
            'password': ''
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Check the keys and try again', response.data.decode())

    def tearDown(self):
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()
