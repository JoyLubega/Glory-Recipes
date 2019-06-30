from flask import json

from .base import BaseCategory
from Api.api import app, db


class CategoryTestcase(BaseCategory):

    def test_add_category_success(self):
        """Should return 201 for category added"""
        category = json.dumps({
            'name': 'Asian',
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('asian', response.data.decode())

    def test_add_category_existing_name(self):
        """Should return 201 for category added"""
        category = json.dumps({
            'name': 'Asian',
         })
        self.client.post('/category', data=category,
                         headers={"Authorization": self.token})
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('Name Asian exists', response.data.decode())

    def test_add_category_empty_name(self):
        """Should return 400 for empty name"""
        category = json.dumps({
            'name': "",
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing name', response.data.decode())

    def test_add_category_space_name(self):
        """Should return 400 for space name"""
        category = json.dumps({
            'name': " ",
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('A space is not a name', response.data.decode())

    def test_add_category_symbol_name(self):
        """Should return 400 for space name"""
        category = json.dumps({
            'name': "Afri@@",
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name should be in alphabetical', response.data.decode())

    def test_add_category_integer_name(self):
        """Should return 400 for space name"""
        category = json.dumps({
            'name': 8888,
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Numbers cant be a Name', response.data.decode())

    def test_add_category_missing_token(self):
        """Should return 400 for space name"""
        category = json.dumps({
            'name': "Jamaican",
         })
        token = ""
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token not found', response.data.decode())

    def test_add_category_missing_fields(self):
        """Should return 400 for space name"""
        category = json.dumps({
            'desc': "Jamaican",
         })
        response = self.client.post('/category', data=category,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Check the keys and try again', response.data.decode())

    def test_get_categories_success(self):
        """Should return 200 for success"""
        self.test_add_category_success()
        response = self.client.get('/categories',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('asian', response.data.decode())

    def test_get_categories_pagination(self):
        """Should return 200 for success"""
        category1 = json.dumps({
            'name': 'Asian',
         })
        category2 = json.dumps({
            'name': 'France',
        })
        category3 = json.dumps({
            'name': 'Chinese',
        })
        category4 = json.dumps({
            'name': 'Ugandan',
        })
        category5 = json.dumps({
            'name': 'Korean',
        })
        category6 = json.dumps({
            'name': 'Western',
        })
        self.client.post('/category', data=category1,
                         headers={"Authorization": self.token})
        self.client.post('/category', data=category2,
                         headers={"Authorization": self.token})
        self.client.post('/category', data=category3,
                         headers={"Authorization": self.token})
        self.client.post('/category', data=category4,
                         headers={"Authorization": self.token})
        self.client.post('/category', data=category5,
                         headers={"Authorization": self.token})
        self.client.post('/category', data=category6,
                         headers={"Authorization": self.token})
        next_page = 'http://localhost/categories?page=2&limit=5'
        response = self.client.get(next_page,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prev', response.data.decode())

    def test_get_categories_not_found(self):
        """Should return 404 for no categories found"""
        response = self.client.get('/categories',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No categories found', response.data.decode())

    def test_get_category_search(self):
        """Should return 200 for no categories found"""
        self.test_add_category_success()
        response = self.client.get('/categories?q=a',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('asian', response.data.decode())

    def test_get_category_invalid_token(self):
        """Should return 200 for no categories found"""
        self.test_add_category_success()
        token = ""
        response = self.client.get('/categories',
                                   headers={"Authorization": token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token not found', response.data.decode())

    def test_get_category_search_not_found(self):
        """Should return 200 for no categories found"""
        self.test_add_category_success()
        response = self.client.get('/categories?q=q',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn('No Categories to display', response.data.decode())

    def test_get_a_category(self):
        """Should return 200 for a category found"""
        self.test_add_category_success()
        response = self.client.get('/categories/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('asian', response.data.decode())

    def test_get_a_category_not_found(self):
        """Should return 404 for a category not found"""
        self.test_add_category_success()
        response = self.client.get('/categories/100',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn('category with id: 100 is not found',
                      response.data.decode())

    def test_get_a_single_category_invalid_token(self):
        """Should return 401 for no categories found"""
        self.test_add_category_success()
        token = ""
        response = self.client.get('/categories/1',
                                   headers={"Authorization": token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token not found', response.data.decode())

    def test_delete_a_category(self):
        """Should return 200 for a category deleted"""
        self.test_add_category_success()
        response = self.client.delete('/categories/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('category deleted permanently',
                      response.data.decode())

    def test_delete_a_category_not_existing(self):
        """Should return 404 for a category not found"""
        response = self.client.delete('/categories/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn('category with id: 1 is not found',
                      response.data.decode())

    def test_delete_a_category_invalid_token(self):
        """Should return 401 for invalid token"""
        self.test_add_category_success()
        token = ""
        response = self.client.delete('/categories/1',
                                      headers={"Authorization": token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token not found', response.data.decode())

    def tearDown(self):
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()
