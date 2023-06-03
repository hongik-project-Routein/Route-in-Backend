import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    def create_user(self, name, password, **kwargs):
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password, **extra_fields):
        superuser = self.create_user(
            name=name,
            password=password,
        )
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    name = models.CharField('NAME', max_length=20, unique=True)
    email = models.EmailField('EMAIL', max_length=40, null=True, blank=True)
    age = models.IntegerField('AGE', null=True, blank=True)

    GENDER_CHOICES = ( ('M', 'Male'), ('F', 'Female') )
    gender = models.CharField('GENDER', max_length=1, choices=GENDER_CHOICES)

    def upload_to_func(instance, filename):
        prefix = timezone.now().strftime("%Y/%m/%d")
        file_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        return "/".join(
            [prefix, file_name, extension, ]
        )
    image = models.ImageField('IMAGE', upload_to=upload_to_func, blank=True)

    follower_set = models.ManyToManyField('self', blank=True)
    following_set = models.ManyToManyField('self', blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser