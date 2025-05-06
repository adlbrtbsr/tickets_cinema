from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=26)
    is_for_adults = models.BooleanField(default=False)


class Actor(models.Model):
    name = models.CharField(max_length=60)
    age = models.PositiveIntegerField()
    nationality = models.CharField(max_length=54)


class Movie(models.Model):
    title = models.CharField(max_length=185)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    duration = models.PositiveIntegerField()


class CinemaHall(models.Model):
    name = models.CharField(max_length=20)


class Seat(models.Model):
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT)


class MovieScreening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField()
    hall = models.ForeignKey(CinemaHall, on_delete=models.PROTECT)


class Ticket(models.Model):
    movie_screening = models.ForeignKey(MovieScreening, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
