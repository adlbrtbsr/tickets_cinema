from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)
    genre_is_for_adults = models.BooleanField(default=False)


class Actor(models.Model):
    actor_name = models.CharField(max_length=100)
    actor_age = models.PositiveIntegerField()
    actor_nationality = models.CharField(max_length=100)


class Movie(models.Model):
    movie_title = models.CharField(max_length=100)
    movie_genres = models.ManyToManyField(Genre)
    movie_actors = models.ManyToManyField(Actor)
    movie_duration = models.PositiveIntegerField()


class CinemaHall(models.Model):
    cinema_hall_name = models.CharField(max_length=100)


class Seat(models.Model):
    seat_row = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    seat_hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT)


class MovieScreening(models.Model):
    movie_screening_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_screening_date = models.DateTimeField()
    movie_screening_hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT)


class Ticket(models.Model):
    ticket_movie_screening = models.ForeignKey(MovieScreening, on_delete=models.CASCADE)
    ticket_seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    ticket_price = models.PositiveIntegerField()
