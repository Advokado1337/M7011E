# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

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
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    stars = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"Rating by {self.user.name} for {self.movie.name}"

    class Meta:
        db_table = 'app_rating'  # Custom table name for migration consistency
