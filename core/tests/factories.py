import factory
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from core.models import Actor, CinemaHall, Genre, Movie, MovieScreening, Seat, Ticket


class ActorFactory(DjangoModelFactory):
    class Meta:
        model = Actor

    name = Faker("name")
    age = Faker("random_int", min=1, max=100)
    nationality = Faker("country")


class CinemaHallFactory(DjangoModelFactory):
    class Meta:
        model = CinemaHall

    name = Faker("pystr", min_chars=2, max_chars=20)


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = Faker("word")
    is_for_adults = Faker("pybool")


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker("sentence", nb_words=5)
    duration = Faker("random_int", min=30, max=200)

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.genres.add(*extracted)
        else:
            self.genres.add(GenreFactory())

    @factory.post_generation
    def actors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.actors.add(*extracted)
        else:
            self.actors.add(ActorFactory())


class MovieScreeningFactory(DjangoModelFactory):
    class Meta:
        model = MovieScreening

    movie = factory.SubFactory(MovieFactory)
    date = Faker("date_time")
    hall = factory.SubFactory(CinemaHallFactory)


class SeatFactory(DjangoModelFactory):
    class Meta:
        model = Seat

    row = Faker("random_int", min=1, max=25)
    number = Faker("random_int", min=1, max=40)
    hall = SubFactory(CinemaHallFactory)


class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket

    movie_screening = SubFactory(MovieScreeningFactory)
    seat = SubFactory(SeatFactory)
    price = Faker("random_int", min=5, max=100)
