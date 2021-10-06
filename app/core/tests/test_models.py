from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

	def test_create_user_with_email_successful(self):
		"""test creating a new user with an email is successful"""

		email = 'test@gmail.com'
		password = 'Testpass123'

		# create the user
		user = get_user_model().objects.create_user(email=email, password=password)

		# check the created users email is the email provided
		self.assertEqual(user.email, email)

		# check the created users password is the password provided
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""Test the users email is normalized"""

		email = 'test@LONDONAPPDEV.COM'
		user = get_user_model().objects.create_user(email, 'test123')

		self.assertEqual(user.email, email.lower())


	def test_new_user_invalid_email(self):
		"""Test creating user with no email raises error"""

		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, 'test123')


	def test_create_super_user(self):
		"""Test creating a new superuser"""

		email = 'test@LONDONAPPDEV.COM'

		user = get_user_model().objects.create_superuser(email, 'test123')

		self.assertTrue(user.is_staff)

		self.assertTrue(user.is_superuser)		

