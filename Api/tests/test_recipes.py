from flask import json

from .base import BaseCategory
from Api.api import app, db


class RecipeTestcase(BaseCategory):

    def test_add_recipe_success(self):
        """Should return 201 for recipe added"""
        category = json.dumps(
            {
                'name': 'Asian',
            }
        )
        recipe = json.dumps(
            {
                'name_of_recipe': 'grilled chicken',
                'recipe_text': "clean the chicken"
            }
        )
        self.client.post('/category', data=category,
                         headers={"Authorization": self.token})
        response = self.client.post('/categories/1/recipe', data=recipe,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('grilled chicken', response.data.decode())

    def test_add_recipe_no_name(self):
        """Should return 400 for recipe not added"""
        category = json.dumps(
            {
                'name': 'Asian',
            }
        )
        recipe = json.dumps(
            {
                'name': 'grilled chicken',
                'recipe_text': "clean the chicken"
            }
        )
        self.client.post('/category', data=category,
                         headers={"Authorization": self.token})
        response = self.client.post('/categories/1/recipe', data=recipe,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Check the keys and try again', response.data.decode())

    def test_add_recipe_same_name(self):
        """Should return 400 for recipe not added"""
        category = json.dumps(
            {
                'name': 'Asian',
            }
        )
        recipe = json.dumps(
            {
                'name_of_recipe': 'grilled chicken',
                'recipe_text': "clean the chicken"
            }
        )
        self.client.post('/category', data=category,
                         headers={"Authorization": self.token})
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token})
        response = self.client.post('/categories/1/recipe', data=recipe,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('Recipe name Already exists', response.data.decode())

    def test_add_recipe_no_category(self):
        """Should return 400 for no category"""
        recipe = json.dumps(
            {
                'name_of_recipe': 'grilled chicken',
                'recipe_text': "clean the chicken"
            }
        )
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token})
        response = self.client.post('/categories/1/recipe', data=recipe,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found', response.data.decode())

    def tearDown(self):
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()
