from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**param):
	"""Helper function for creating users"""

	return get_user_model().objects.create_user(**param)

class PublicUserApiTests(TestCase):
	"""Test the users API (public)"""

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_user_success(self):
		"""Test creating the user with valid data is successful"""

		payload = {
			'email': 'test@banks.com',
			'password': 'testpass',
			'name': 'Test name'
		}

		res = self.client.post(CREATE_USER_URL, payload)

		# check for successful http status code
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		user = get_user_model().objects.get(**res.data)

		# check created user password is correct
		self.assertTrue(user.check_password(payload['password']))

		# check password not in the data returned
		self.assertNotIn('password', res.data)


	def test_user_exists(self):
		"""Test creating user that already exists"""

		payload = {
			'email': 'test@banks.com',
			'password': 'testpass',
			'name': 'Test name'
		}	 	

		# create user with payload
		create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_password_too_short(self):
		"""Test that the password must be more than 5 chars"""

		payload = {
			'email': 'test@banks.com',
			'password': 'pw',
			'name': 'Test name'
		}

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

		user_exists = get_user_model().objects.filter(
			email = payload['email'],
		).exists()

		self.assertFalse(user_exists)


	def test_create_token_for_user(self):
		"""Test that a token is created for the user"""

		payload = {
			'email': 'test@banks.com',
			'password': 'testpass',
		}

		create_user(**payload)

		res = self.client.post(TOKEN_URL, payload)

		self.assertIn('token', res.data)

		self.assertEqual(res.status_code, status.HTTP_200_OK)


	def test_create_token_invalid_credentials(self):
		"""Test that token is not created if invalid credentials are given"""

		payload = {
			'email': 'test@banks.com',
			'password': 'testpass',
			'name': 'Test name'
		}

		create_user(**payload)

		invalid_payload = {'email': 'test@banks.com', 'password': 'wrong'}

		res = self.client.post(TOKEN_URL, invalid_payload)

		self.assertNotIn('token', res.data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_create_token_no_user(self):
		"""Test that token is not created if user doesnt exist"""

		payload = {
			'email': 'test@banks.com',
			'password': 'testpass',
		}

		res = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', res.data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_create_token_missing_field(self):
		"""Test that email and password are required"""

		res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

		self.assertNotIn('token', res.data)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
	




