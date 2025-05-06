from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=50)
    is_for_adults = models.BooleanField(default=False)


class Actor(models.Model):
    name = models.CharField(max_length=80)
    age = models.PositiveSmallIntegerField(help_text="Age of the actor in years")
    nationality = models.CharField(max_length=54)


class Movie(models.Model):
    title = models.CharField(max_length=185)
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    duration = models.PositiveIntegerField(help_text="Duration of the movie in minutes")


class CinemaHall(models.Model):
    name = models.CharField(max_length=20)


class Seat(models.Model):
    row = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT, related_name="seat")


class MovieScreening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name="movie_screening")
    date = models.DateTimeField()
    hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT, related_name="movie_screening")


class Ticket(models.Model):
    movie_screening = models.ForeignKey(MovieScreening, on_delete=models.CASCADE, related_name="ticket")
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, related_name="ticket")
    price = models.PositiveSmallIntegerField(help_text="Price of the ticket in PLN")
