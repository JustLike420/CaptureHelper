import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# def user_directory_path(instance: 'User', filename: str) -> str:
#     """Generate path to file in upload"""
#     return f'users/avatar/user_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'
#
#
# class User(AbstractUser):
#     """User model override"""
#     email = models.EmailField(unique=False, blank=True, null=True)
#     avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
#     # clan = models.ForeignKey()
#     # REQUIRED_FIELDS = []
#     USERNAME_FIELD = "username"
#
#     def save(self, *args, **kwargs):
#         self.set_password(self.password)
#         super(User, self).save(*args, **kwargs)

