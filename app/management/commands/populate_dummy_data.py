from django.core.management.base import BaseCommand
from app.models import Users, Category, Movie, MovieCategory, MovieDirector, MovieDirectorAssignment, Description, Rating

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create Users
        user1, created = Users.objects.get_or_create(username='john_doe', defaults={'password': 'password123'})
        user2, created = Users.objects.get_or_create(username='jane_smith', defaults={'password': 'password456'})

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

        # Create Descriptions
        Description.objects.get_or_create(movie=movie1, defaults={'description': 'An epic adventure movie.'})
        Description.objects.get_or_create(movie=movie2, defaults={'description': 'A hilarious comedy movie.'})
        Description.objects.get_or_create(movie=movie3, defaults={'description': 'A touching drama movie.'})

        # Create Ratings
        Rating.objects.get_or_create(movie=movie1, user=user1, defaults={'stars': 5, 'text': 'Amazing movie!'})
        Rating.objects.get_or_create(movie=movie2, user=user2, defaults={'stars': 4, 'text': 'Really funny!'})
        Rating.objects.get_or_create(movie=movie3, user=user1, defaults={'stars': 3, 'text': 'Quite emotional.'})

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))