from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Rating, Ingredient, Instruction


class RecipeTests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a recipe
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            description='This is a test recipe'
        )
        
        # Create ingredients and instructions for the recipe
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            quantity='1 cup',
            recipe=self.recipe
        )
        
        self.instruction = Instruction.objects.create(
            step_number=1,
            description='This is a test instruction',
            recipe=self.recipe
        )

    def test_create_recipe(self):
        url = reverse('recipe-list-create')
        data = {
            'title': 'New Test Recipe',
            'description': 'This is another test recipe',
            'ingredients': [{'name': 'Test ingredient 1', 'quantity': '1 spoon'}],
            'instructions': [{'step_number': 1, 'description': 'Test instruction 1'}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        
    def test_list_recipes(self):
        url = reverse('recipe-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_rate_recipe(self):
        url = reverse('rating-create')
        data = {'recipe': self.recipe.id, 'rating': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        
    def test_rate_recipe_twice(self):
        url = reverse('rating-create')
        data = {'recipe': self.recipe.id, 'rating': 5}
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
