from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
	"""Customize the base user django manager"""

	def create_user(self, email, password=None, **extra_fields):
		"""Creates and saves a new user with the email & password"""

		if not email:
			raise ValueError('Users must have an email address')

		# create the user
		user = self.model(email=self.normalize_email(email), **extra_fields)

		# set the users password
		user.set_password(password)

		# save the user to the db
		user.save(using=self.db)

		return user

	def create_superuser(self, email, password):
		"""Creates a new superuser"""

		user = self.create_user(email, password)

		user.is_staff = True

		user.is_superuser = True

		user.save(using=self._db)

		return user	


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom user model that uses email insted of username"""

	email = models.EmailField(unique=True, max_length=255)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'