import datetime

import pytest
from freezegun import freeze_time

from core.tests.factories import ActorFactory, CinemaHallFactory, GenreFactory, MovieFactory, MovieScreeningFactory, \
    SeatFactory, TicketFactory

class TestModels:
    pytestmark = pytest.mark.django_db
    def test_actor(self):
        actor = ActorFactory(name="Marcin Sarepski", age=27, nationality="Polish")
        assert actor.name == "Marcin Sarepski"
        assert actor.age == 27
        assert actor.nationality == "Polish"

    def test_cinema_hall(self):
        cinema_hall = CinemaHallFactory(name="Cinema Hall")
        assert cinema_hall.name == "Cinema Hall"

    def test_genre(self):
        genre = GenreFactory(name="Science Fiction", is_for_adults=True)
        assert genre.name == "Science Fiction"
        assert genre.is_for_adults == True

    def test_movie(self):
        movie = MovieFactory(title="Cars", duration=120,
                             genres=[
                                 GenreFactory(name="Animation", is_for_adults=False),
                                 GenreFactory(name="Kids", is_for_adults=False),
                             ],
                             actors=[
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="Marcin Sarepski", age=27, nationality="Polish"),
                             ])
        assert movie.title == "Cars"
        assert movie.duration == 120
        assert movie.genres.count() == 2
        assert movie.genres.first().name == "Animation"
        assert movie.genres.last().is_for_adults == False
        assert movie.actors.count() == 3
        assert movie.actors.last().name == "Marcin Sarepski"
        assert movie.actors.last().age == 27
        assert movie.actors.last().nationality == "Polish"

    @freeze_time("2027-05-18")
    def test_movie_screening(self):
        movie_screening = MovieScreeningFactory(movie=MovieFactory(title="Cars", duration=120,
                             genres=[
                                 GenreFactory(name="Animation", is_for_adults=False),
                                 GenreFactory(name="Kids", is_for_adults=False),
                             ],
                             actors=[
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="Marcin Sarepski", age=27, nationality="Polish"),
                             ]),
                                                date=datetime.datetime.now(),
                                                hall=CinemaHallFactory(name="Cinema Hall"))
        assert movie_screening.movie.title == "Cars"
        assert movie_screening.movie.duration == 120
        assert movie_screening.movie.actors.last().age == 27
        assert movie_screening.movie.actors.last().nationality == "Polish"
        assert movie_screening.date == datetime.datetime(2027, 5, 18)
        assert movie_screening.hall.name == "Cinema Hall"

    def test_seat(self):
        seat = SeatFactory(row=21, number=37, hall=CinemaHallFactory(name="Cinema Hall"))
        assert seat.row == 21
        assert seat.number == 37
        assert seat.hall.name == "Cinema Hall"

    def test_ticket(self):
        ticket = TicketFactory(movie_screening=MovieScreeningFactory(movie=MovieFactory(title="Cars", duration=120,
                             genres=[
                                 GenreFactory(name="Animation", is_for_adults=False),
                                 GenreFactory(name="Kids", is_for_adults=False),
                             ],
                             actors=[
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="<NAME>", age=18, nationality="Polish"),
                                 ActorFactory(name="Marcin Sarepski", age=27, nationality="Polish"),
                             ]),
                                                date=datetime.datetime.now(),
                                                hall=CinemaHallFactory(name="Cinema Hall")),
                               seat=SeatFactory(row=21, number=37, hall=CinemaHallFactory(name="Cinema Hall")),
                               price=19)
        assert ticket.movie_screening.movie.title == "Cars"
        assert ticket.movie_screening.movie.actors.last().name == "Marcin Sarepski"
        assert ticket.seat.row == 21
        assert ticket.seat.number == 37
        assert ticket.seat.hall.name == "Cinema Hall"
        assert ticket.price == 19