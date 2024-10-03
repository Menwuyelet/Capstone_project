from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        user = self.model(email = self.normalize_email(email), username = username)
        user.set_password(password) # handles the hashing and managing passwords
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email = email, username = username, password = password) # calls the Create_user to create 
        user.is_staff = True # add aditional field is_staff
        user.is_superuser = True # add aditional field is_superuser
        user.save(using = self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=15)
    objects = UserManager()
    USERNAME_FIELD = 'email' # the username field used for auth is email
    REQUIRED_FIELDS = ['username'] # user name must be unique and requierd

    def __str__(self):
        return self.username