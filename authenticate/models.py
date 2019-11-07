
from django.db import models
from django.contrib.auth.models import (
BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
	def create_user(self, username, password,coop):
		if not username:
			raise ValueError('Users must have a user name')
		user = self.model(
		username=username,
		coop=coop
		)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, username,password):
		user = self.create_user(
		username,
		password=password,
		coop=''
		)
		user.is_admin = True
		user.coop_admin=False
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	username = models.CharField(max_length=50,unique=True)
	fname = models.CharField(max_length=50,blank=True)
	lname = models.CharField(max_length=50,blank=True)
	phone = models.CharField(max_length=50,blank=True)
	coop = models.CharField(max_length=50,blank=True)
	coop_admin = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'username'
	def __str__(self):
		return self.username
	def has_perm(self, perm, obj=None):
		# Simplest possible answer: Yes, always
		return True
	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin


