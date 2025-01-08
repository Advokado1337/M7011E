from django.core.management.base import BaseCommand
from app.models import Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        user1, created = User.objects.get_or_create(
            username='eric_john',
            email='eric_john@example.com',
            defaults={
                'password': 'password678',
            }
        )
        if created:
            user1.set_password('password678')
            user1.save()
        
        user2, created = User.objects.get_or_create(
            username='john_doe',
            email='john_doe@example.com',
            defaults={
                'password': 'password123',
            }
        )
        if created:
            user2.set_password('password123')
            user2.is_staff = True
            user2.save()

        user3, created = User.objects.get_or_create(
            username='jane_smith',
            email='jane_smith@example.com',
            defaults={
                'password': 'password456',
            }
        )
        if created:
            user3.set_password('password456')
            user3.is_staff = True
            user3.is_superuser = True
            user3.save()

        # Create Categories
        category1, created = Category.objects.get_or_create(category='Action')
        category2, created = Category.objects.get_or_create(category='Comedy')
        category3, created = Category.objects.get_or_create(category='Drama')

        # Create Movies
        movie1, created = Movie.objects.get_or_create(name='The Great Adventure')
        movie2, created = Movie.objects.get_or_create(name='Funny Moments')
        movie3, created = Movie.objects.get_or_create(name='Dramatic Scenes')

        # Assign Categories to Movies
        MovieCategory.objects.get_or_create(movie=movie1, category=category1)
        MovieCategory.objects.get_or_create(movie=movie2, category=category2)
        MovieCategory.objects.get_or_create(movie=movie3, category=category3)

        # Create Directors
        director1, created = MovieDirector.objects.get_or_create(firstname='Steven', surname='Spielberg')
        director2, created = MovieDirector.objects.get_or_create(firstname='Quentin', surname='Tarantino')

        # Assign Directors to Movies
        MovieDirectorAssignment.objects.get_or_create(movie=movie1, director=director1)
        MovieDirectorAssignment.objects.get_or_create(movie=movie2, director=director2)
        MovieDirectorAssignment.objects.get_or_create(movie=movie3, director=director1)

        # Create Descriptions
        Description.objects.get_or_create(movie=movie1, defaults={'description': 'An epic adventure movie.'})
        Description.objects.get_or_create(movie=movie2, defaults={'description': 'A hilarious comedy movie.'})
        Description.objects.get_or_create(movie=movie3, defaults={'description': 'A touching drama movie.'})

        # Create Ratings
        Rating.objects.get_or_create(movie=movie1, user=user1, defaults={'stars': 5, 'text': 'Amazing movie!'})
        Rating.objects.get_or_create(movie=movie2, user=user2, defaults={'stars': 4, 'text': 'Really funny!'})
        Rating.objects.get_or_create(movie=movie3, user=user1, defaults={'stars': 3, 'text': 'Quite emotional.'})

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))