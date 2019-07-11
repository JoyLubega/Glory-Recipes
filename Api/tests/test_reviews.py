from flask import json

from .base import BaseReview
from Api.api import app, db


class ReviewTestcase(BaseReview):

    def test_add_reviews_for_your_recipe(self):
        """Should return 400 for review added"""
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
                         headers={"Authorization": self.token2})
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token2})
        review = json.dumps(
            {
                'comment_text': 'this is a comment',
                'rate': 3
            }
        )

        response = self.client.post('/review/1', data=review,
                                    headers={"Authorization": self.token2})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
                  'You can not rate your own recipe', response.data.decode())

    def test_add_reviews_success(self):
        """Should return 400 for review added"""
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
                         headers={"Authorization": self.token2})
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token2})
        review = json.dumps(
            {
                'comment_text': 'this is a comment',
                'rate': 3
            }
        )

        response = self.client.post('/review/1', data=review,
                                    headers={"Authorization": self.token3})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review added successfully', response.data.decode())

    def test_add_rating_above_5(self):
        """Should return 400 for review not added"""
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
                         headers={"Authorization": self.token2})
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token2})
        review = json.dumps(
            {
                'comment_text': 'this is a comment',
                'rate': 10
            }
        )

        response = self.client.post('/review/1', data=review,
                                    headers={"Authorization": self.token3})
        self.assertEqual(response.status_code, 400)
        self.assertIn('The rating is between 1 to 5', response.data.decode())

    def test_add_reviews_missing_fileld(self):
        """Should return 400 for review not added"""
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
                         headers={"Authorization": self.token2})
        self.client.post('/categories/1/recipe', data=recipe,
                         headers={"Authorization": self.token2})
        review = json.dumps(
            {
                'comment_text': 'this is a comment'
            }
        )

        response = self.client.post('/review/1', data=review,
                                    headers={"Authorization": self.token3})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Check the keys and try again', response.data.decode())
        # def test_add_recipe_no_name(self):
    #     """Should return 400 for recipe not added"""
    #     category = json.dumps(
    #         {
    #             'name': 'Asian',
    #         }
    #     )
    #     recipe = json.dumps(
    #         {
    #             'name': 'grilled chicken',
    #             'recipe_text': "clean the chicken"
    #         }
    #     )
    #     self.client.post('/category', data=category,
    #                      headers={"Authorization": self.token})
    #     response = self.client.post('/categories/1/recipe', data=recipe,
    #                                 headers={"Authorization": self.token})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('Check the keys and try again', response.data.decode())

    # def test_add_recipe_same_name(self):
    #     """Should return 400 for recipe not added"""
    #     category = json.dumps(
    #         {
    #             'name': 'Asian',
    #         }
    #     )
    #     recipe = json.dumps(
    #         {
    #             'name_of_recipe': 'grilled chicken',
    #             'recipe_text': "clean the chicken"
    #         }
    #     )
    #     self.client.post('/category', data=category,
    #                      headers={"Authorization": self.token})
    #     self.client.post('/categories/1/recipe', data=recipe,
    #                      headers={"Authorization": self.token})
    #     response = self.client.post('/categories/1/recipe', data=recipe,
    #                                 headers={"Authorization": self.token})
    #     self.assertEqual(response.status_code, 409)
    #     self.assertIn('Recipe name Already exists', response.data.decode())

    # def test_add_recipe_no_category(self):
    #     """Should return 400 for no category"""
    #     recipe = json.dumps(
    #         {
    #             'name_of_recipe': 'grilled chicken',
    #             'recipe_text': "clean the chicken"
    #         }
    #     )
    #     self.client.post('/categories/1/recipe', data=recipe,
    #                      headers={"Authorization": self.token})
    #     response = self.client.post('/categories/1/recipe', data=recipe,
    #                                 headers={"Authorization": self.token})
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('Category not found', response.data.decode())

    def tearDown(self):
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()
