# from django.db import models
# from django.contrib.auth.models import AbstractUser, PermissionsMixin
# from django.contrib.auth.base_user import BaseUserManager
# from socialmedia.models import BaseModel
#
#
# class User(BaseModel, AbstractUser, PermissionsMixin):
#     name = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(max_length=40, null=True, blank=True)
#     age = models.IntegerField(unique=True)
#
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, unique=True)
#
#     def upload_to_func(instance, filename):
#     prefix = timezone.now().strftime("%Y/%m/%d")
#     file_name = uuid4().hex
#     extension = os.path.splitext(filename)[-1].lower()
#     return "/".join(
#         [prefix, file_name, extension, ]
#     )
#     image = models.ImageField('IMAGE', upload_to=upload_to_func)
#
#     follower_set = models.ManyToManyField('self', blank=True)
#     following_set = models.ManyToManyField('self', blank=True)
#
#     is_active = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password, **kwargs):
#         user = self.model(
#             email=email,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         superuser = self.create_user(
#             email=email,
#             password=password,
#         )
#         superuser.is_superuser = True
#         superuser.is_active = True
#         superuser.save(using=self._db)
#         return superuser