from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create') #user --> app, create --> end point #API URL that will be tested in this file
TOKEN_URL = reverse('users:token')

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

    #Test generates token for valid credentials.
    def test_create_token_for_user(self):

        #CREATING NEW USER WITH THIS DETAILS
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        #CREATING NEW USER WITH above details
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        #tesing API endpoint for login(post payload to the token url)
        self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data) #checks res.data includes a token
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)


        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




