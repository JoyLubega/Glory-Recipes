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
