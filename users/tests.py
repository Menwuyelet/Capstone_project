from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import User


class AuthAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com'
        )

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        }
        # send request to the end point
        response = self.client.post(reverse('signup'), data)

        # Assert response status and user creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_register_duplicate_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        }
        # send request to the end point
        response = self.client.post(reverse('signup'), data)

        # Assert response status and user creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

        duplicate_response = self.client.post(reverse('signup'), data)

        # Assert that the second registration fails (e.g., HTTP 400 Bad Request)
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure that only one user was created
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_register_invalid_user(self):
        data = {
            'username': 'newuser1',
            'password': 'newpass1',
            'email': 'newuser@example'
        }
        # send request to the end point
        response = self.client.post(reverse('signup'), data)

        # Assert response status and user creation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username='newuser1').count(), 0)
        
    def test_login_user(self):
        # Define login credentials
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass'
        }

        # Send POST request to login
        response = self.client.post(reverse('login'), data)

        # Assert response status and token presence
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_user(self):
        # Define login credentials
        data = {
            'email': 'testuser1@example.com',
            'password': 'testpass'
        }

        # Send POST request to login
        response = self.client.post(reverse('login'), data)

        # Assert response status and token presence
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("No active account found with the given credentials", response.data['detail'])
       
    def test_refresh_token(self):
        # Log in to obtain tokens
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass'
        }
        login_response = self.client.post(reverse('login'), login_data)
        refresh_token = login_response.data['refresh']

        # Send POST request to refresh token
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})

        # Assert response status and new access token
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_refresh_token(self):

        refersh = "inavalid refresh token."
        refresh_token = refersh

        # Send POST request to refresh token with invalid token
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})

        # Assert response status 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('token_not_valid', response.data['code'])

    def test_logout_user(self):
        # Log in to obtain tokens
        login_data = {
            'email': 'testuser@example.com',  # Ensure you're using the correct field for username
            'password': 'testpass'
        }
        login_response = self.client.post(reverse('login'), login_data)

        # Extract the tokens from the login response
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']  # Get the refresh token

        # Set the access token in the Authorization header for the logout request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Send POST request to logout with refresh token in the body
        logout_response = self.client.post(reverse('logout'), data={'refresh': refresh_token})


        # Assert response status
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_logout_unauthenticated_user(self):
        # Attempt to log out without being logged in
        response = self.client.post(reverse('logout'))

        # Assert the response status and message
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Authentication credentials were not provided", response.data['detail'])

        error_detail = response.data["detail"]
        self.assertEqual(error_detail.code, 'not_authenticated') 
        
    def test_delete_user(self):
        # Log in to obtain tokens
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass'
        }
        login_response = self.client.post(reverse('login'), login_data)
        access_token = login_response.data['access']

        # Set the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Send DELETE request to delete the user
        response = self.client.delete(reverse('delete_user'))

        # Assert response status and user deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username='testuser').count(), 0)

    def test_delete_unauthenticated_user(self):
        # Attempt to log out without being logged in
        response = self.client.post(reverse('delete_user'))

        # Assert the response status and message
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Authentication credentials were not provided", response.data['detail'])

        error_detail = response.data["detail"]
        self.assertEqual(error_detail.code, 'not_authenticated') 