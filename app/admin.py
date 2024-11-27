from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from app.models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating

# Register your models here.
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(MovieCategory)
admin.site.register(MovieDirector)
admin.site.register(MovieDirectorAssignment)
admin.site.register(Description)
admin.site.register(Rating)

# Register the Token model if not already registered
try:
    admin.site.register(Token)
except admin.sites.AlreadyRegistered:
    pass