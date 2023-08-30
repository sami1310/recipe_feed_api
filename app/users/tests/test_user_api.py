from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framewrok.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create') #user --> app, create --> end point #API URL that will be tested in this file

#helper function to create user
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


#function for public tests(Ie: Unauthencitated requests)
class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient() #Creats API clients for tesing purpose

    def test_create_user_success(self):
    #variables needed for creating new users
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload) #MAKING POST REQUEST TO THE URL USING PAYLOAD INFO

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) #STATUS CODE RETURNS

        user = get_user_model().objects.get(email=payload['email']) #retrives the created user and validates that the object was created
        self.assertTrue(user.check_password(payload['password'])) #testing that the password is correct
        self.assertNotIn('password', res.data) #ensures that the password is not returned in the response


    def test_user_with_email_exists_error(self):

        #variables needed for creating new users
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):

        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)





