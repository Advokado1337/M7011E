# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User


# ROLE_CHOICES = (
#     (1, 'Admin'),
#     (2, 'SuperUser'),
#     (3, 'User'),
# )

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     created_date = models.DateTimeField(default=timezone.now)
#     modified_date = models.DateTimeField(default=timezone.now)

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_groups',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups',
#     )

#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class Movie(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MovieCategory(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'category')
        db_table = 'app_moviecategory'  # Custom table name for migration consistency


class MovieDirector(models.Model):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstname} {self.surname}"


class MovieDirectorAssignment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey(MovieDirector, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'director')
        db_table = 'app_moviedirectorassignment'  # Custom table name for migration consistency


class Description(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Description for {self.movie.name}"





class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"Rating by {self.user.name} for {self.movie.name}"

    class Meta:
        db_table = 'app_rating'  # Custom table name for migration consistency
