from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from socialmedia.models import BaseModel


# class customUser(BaseModel, AbstractBaseUser, PermissionsMixin):
#     # # id
#     # # password
#     name = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(max_length=30, null=True, blank=True)
#     age = models.IntegerField(unique=True)
#
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, unique=True)
#
#     # followers = models.ManyToManyField()
#     # # last_login
#     is_active = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
