from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from core.models import (
    Actor,
    CinemaHall,
    Genre,
    Movie,
    MovieScreening,
    Seat,
    Ticket,
)
from core.serializers import (
    ActorSerializer,
    CinemaHallSerializer,
    GenreSerializer,
    SeatSerializer,
)
from core.tests.factories import (
    ActorFactory,
    CinemaHallFactory,
    GenreFactory,
    MovieFactory,
    MovieScreeningFactory,
    SeatFactory,
    TicketFactory,
)


@pytest.mark.django_db
class TestGenre:
    url_list = reverse("genre-list")

    def test_genre_post(self, client):
        genre = GenreFactory.build()
        serialized = GenreSerializer(genre).data

        response = client.post(
            self.url_list, data=serialized, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["name"] == serialized["name"]
        assert response_data["is_for_adults"] == serialized["is_for_adults"]
        assert Genre.objects.filter(name=serialized["name"]).exists()
        assert set(response_data.keys()) == {"id", "name", "is_for_adults"}

    def test_genre_post_blank(self, client):
        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == {"name": ["This field is required."]}

    def test_genre_post_invalid_name(self, client):
        response = client.post(
            self.url_list, data={"name": "a" * 51}, content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json() == {
            "name": ["Ensure this field has no more than 50 characters."]
        }

    def test_genre_get_list(self, client):
        genre1 = GenreFactory.create()
        genre2 = GenreFactory.create()

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 2
        assert {"id", "name", "is_for_adults"} <= set(response_data[0].keys())

    def test_genre_get_detail(self, client):
        genre = GenreFactory.create()
        url = reverse("genre-detail", args=[genre.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == genre.name

    def test_genre_put(self, client):
        genre = GenreFactory.create()
        url = reverse("genre-detail", args=[genre.id])
        updated_data = {"name": "Updated Genre", "is_for_adults": True}

        response = client.put(url, data=updated_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == updated_data["name"]
        assert response_data["is_for_adults"] == updated_data["is_for_adults"]

    def test_genre_delete(self, client):
        genre = GenreFactory.create()
        url = reverse("genre-detail", args=[genre.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not Genre.objects.filter(id=genre.id).exists()


@pytest.mark.django_db
class TestActor:
    url_list = reverse("actor-list")

    def test_actor_post(self, client):
        actor = ActorFactory.build()
        serialized = ActorSerializer(actor).data

        response = client.post(
            self.url_list, data=serialized, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["name"] == serialized["name"]
        assert response_data["age"] == serialized["age"]
        assert response_data["nationality"] == serialized["nationality"]
        assert Actor.objects.filter(name=serialized["name"]).exists()

    def test_actor_post_blank(self, client):
        expected = {
            "name": ["This field is required."],
            "age": ["This field is required."],
            "nationality": ["This field is required."],
        }

        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == expected

    def test_actor_post_invalid_name(self, client):
        data = {
            "name": "a" * 81,
            "age": 30,
            "nationality": "TestCountry",
        }

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json() == {
            "name": ["Ensure this field has no more than 80 characters."]
        }

    def test_actor_get_list(self, client):
        ActorFactory.create()
        ActorFactory.create()
        expected_keys = {"id", "name", "age", "nationality"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 2
        assert expected_keys == set(response_data[0].keys())

    def test_actor_get_detail(self, client):
        actor = ActorFactory.create()
        url = reverse("actor-detail", args=[actor.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == actor.name

    def test_actor_put(self, client):
        actor = ActorFactory.create()
        url = reverse("actor-detail", args=[actor.id])
        new_data = {
            "name": "Updated Actor",
            "age": actor.age + 1,
            "nationality": actor.nationality,
        }

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == new_data["name"]
        assert response_data["age"] == new_data["age"]
        assert response_data["nationality"] == new_data["nationality"]

    def test_actor_delete(self, client):
        actor = ActorFactory.create()
        url = reverse("actor-detail", args=[actor.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not Actor.objects.filter(id=actor.id).exists()


@pytest.mark.django_db
class TestMovie:
    url_list = reverse("movie-list")

    def test_movie_post(self, client):
        genre = GenreFactory.create()
        actor = ActorFactory.create()
        data = {
            "title": "Test Movie",
            "duration": 120,
            "genres": [genre.id],
            "actors": [actor.id],
        }

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["title"] == data["title"]
        assert response_data["duration"] == data["duration"]
        assert genre.id in response_data["genres"]
        assert actor.id in response_data["actors"]

    def test_movie_post_blank(self, client):
        response = client.post(self.url_list, data={}, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 400
        assert "title" in response_data
        assert "duration" in response_data

    def test_movie_post_invalid_title(self, client):
        genre = GenreFactory.create()
        actor = ActorFactory.create()
        data = {
            "title": "a" * 186,
            "duration": 100,
            "genres": [genre.id],
            "actors": [actor.id],
        }

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json() == {
            "title": ["Ensure this field has no more than 185 characters."]
        }

    def test_movie_get_list(self, client):
        MovieFactory.create()
        MovieFactory.create()
        expected_keys = {"id", "title", "genres", "actors", "duration"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert expected_keys == set(response_data[0].keys())

    def test_movie_get_detail(self, client):
        movie = MovieFactory.create()
        url = reverse("movie-detail", args=[movie.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["title"] == movie.title

    def test_movie_put(self, client):
        movie = MovieFactory.create()
        url = reverse("movie-detail", args=[movie.id])
        genre = GenreFactory.create()
        actor = ActorFactory.create()
        new_data = {
            "title": "Updated Movie",
            "duration": movie.duration + 10,
            "genres": [genre.id],
            "actors": [actor.id],
        }

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["title"] == new_data["title"]
        assert response_data["duration"] == new_data["duration"]
        assert genre.id in response_data["genres"]
        assert actor.id in response_data["actors"]

    def test_movie_delete(self, client):
        movie = MovieFactory.create()
        url = reverse("movie-detail", args=[movie.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not Movie.objects.filter(id=movie.id).exists()


@pytest.mark.django_db
class TestCinemaHall:
    url_list = reverse("cinema-hall-list")

    def test_cinema_hall_post(self, client):
        hall = CinemaHallFactory.build()
        serialized = CinemaHallSerializer(hall).data

        response = client.post(
            self.url_list, data=serialized, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["name"] == serialized["name"]
        assert CinemaHall.objects.filter(name=serialized["name"]).exists()

    def test_cinema_hall_post_blank(self, client):
        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == {"name": ["This field is required."]}

    def test_cinema_hall_post_invalid_name(self, client):
        data = {"name": "a" * 21}

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json() == {
            "name": ["Ensure this field has no more than 20 characters."]
        }

    def test_cinema_hall_get_list(self, client):
        CinemaHallFactory.create()
        CinemaHallFactory.create()
        expected_keys = {"id", "name"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert expected_keys == set(response_data[0].keys())

    def test_cinema_hall_get_detail(self, client):
        hall = CinemaHallFactory.create()
        url = reverse("cinema-hall-detail", args=[hall.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == hall.name

    def test_cinema_hall_put(self, client):
        hall = CinemaHallFactory.create()
        url = reverse("cinema-hall-detail", args=[hall.id])
        new_data = {"name": "Updated Hall"}

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == new_data["name"]

    def test_cinema_hall_delete(self, client):
        hall = CinemaHallFactory.create()
        url = reverse("cinema-hall-detail", args=[hall.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not CinemaHall.objects.filter(id=hall.id).exists()


@pytest.mark.django_db
class TestSeat:
    url_list = reverse("seat-list")

    def test_seat_post(self, client):
        hall = CinemaHallFactory.create()
        seat = SeatFactory.build(hall=hall)
        serialized = SeatSerializer(seat).data

        response = client.post(
            self.url_list, data=serialized, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["row"] == serialized["row"]
        assert response_data["number"] == serialized["number"]
        assert Seat.objects.filter(
            row=serialized["row"], number=serialized["number"]
        ).exists()

    def test_seat_post_blank(self, client):
        expected = {
            "row": ["This field is required."],
            "number": ["This field is required."],
            "hall": ["This field is required."],
        }

        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == expected

    def test_seat_post_invalid(self, client):
        hall = CinemaHallFactory.create()
        data = {"row": -1, "number": 5, "hall": hall.id}

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        json_data = response.json()

        assert response.status_code == 400
        assert "row" in json_data

    def test_seat_get_list(self, client):
        SeatFactory.create()
        SeatFactory.create()
        expected_keys = {"id", "row", "number", "hall"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert expected_keys == set(response_data[0].keys())

    def test_seat_get_detail(self, client):
        seat = SeatFactory.create()
        url = reverse("seat-detail", args=[seat.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["row"] == seat.row

    def test_seat_put(self, client):
        seat = SeatFactory.create()
        url = reverse("seat-detail", args=[seat.id])
        new_data = {"row": seat.row + 1, "number": seat.number, "hall": seat.hall.id}

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["row"] == new_data["row"]

    def test_seat_delete(self, client):
        seat = SeatFactory.create()
        url = reverse("seat-detail", args=[seat.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not Seat.objects.filter(id=seat.id).exists()


@pytest.mark.django_db
class TestMovieScreening:
    url_list = reverse("screening-list")

    def test_movie_screening_post(self, client):
        movie = MovieFactory.create()
        hall = CinemaHallFactory.create()
        screening_date = (timezone.now() + timedelta(days=1)).isoformat()
        data = {
            "movie": movie.id,
            "date": screening_date,
            "hall": hall.id,
        }

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["movie"] == data["movie"]
        assert response_data["hall"] == data["hall"]

    def test_movie_screening_post_blank(self, client):
        expected = {
            "movie": ["This field is required."],
            "date": ["This field is required."],
            "hall": ["This field is required."],
        }

        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == expected

    def test_movie_screening_post_invalid_date(self, client):
        movie = MovieFactory.create()
        hall = CinemaHallFactory.create()
        data = {"movie": movie.id, "date": "invalid-date", "hall": hall.id}

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        json_data = response.json()

        assert response.status_code == 400
        assert "date" in json_data

    def test_movie_screening_get_list(self, client):
        MovieScreeningFactory.create()
        MovieScreeningFactory.create()
        expected_keys = {"id", "movie", "date", "hall"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert expected_keys == set(response_data[0].keys())

    def test_movie_screening_get_detail(self, client):
        screening = MovieScreeningFactory.create()
        url = reverse("screening-detail", args=[screening.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == screening.id

    def test_movie_screening_put(self, client):
        screening = MovieScreeningFactory.create()
        url = reverse("screening-detail", args=[screening.id])
        new_movie = MovieFactory.create()
        new_hall = CinemaHallFactory.create()
        new_date = (timezone.now() + timedelta(days=2)).isoformat()
        new_data = {"movie": new_movie.id, "date": new_date, "hall": new_hall.id}

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["movie"] == new_data["movie"]
        assert response_data["hall"] == new_data["hall"]

    def test_movie_screening_delete(self, client):
        screening = MovieScreeningFactory.create()
        url = reverse("screening-detail", args=[screening.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not MovieScreening.objects.filter(id=screening.id).exists()


@pytest.mark.django_db
class TestTicket:
    url_list = reverse("ticket-list")

    def test_ticket_post(self, client):
        screening = MovieScreeningFactory.create()
        seat = SeatFactory.create()
        data = {"movie_screening": screening.id, "seat": seat.id, "price": 20}

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["movie_screening"] == data["movie_screening"]
        assert response_data["seat"] == data["seat"]
        assert response_data["price"] == data["price"]

    def test_ticket_post_blank(self, client):
        expected = {
            "movie_screening": ["This field is required."],
            "price": ["This field is required."],
        }

        response = client.post(self.url_list, data={}, content_type="application/json")

        assert response.status_code == 400
        assert response.json() == expected

    def test_ticket_post_invalid_price(self, client):
        screening = MovieScreeningFactory.create()
        seat = SeatFactory.create()
        data = {"movie_screening": screening.id, "seat": seat.id, "price": -10}

        response = client.post(
            self.url_list, data=data, content_type="application/json"
        )
        json_data = response.json()

        assert response.status_code == 400
        assert "price" in json_data

    def test_ticket_get_list(self, client):
        TicketFactory.create()
        TicketFactory.create()
        expected_keys = {"id", "movie_screening", "seat", "price"}

        response = client.get(self.url_list)
        response_data = response.json()

        assert response.status_code == 200
        assert expected_keys == set(response_data[0].keys())

    def test_ticket_get_detail(self, client):
        ticket = TicketFactory.create()
        url = reverse("ticket-detail", args=[ticket.id])

        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == ticket.id

    def test_ticket_put(self, client):
        ticket = TicketFactory.create()
        url = reverse("ticket-detail", args=[ticket.id])
        new_screening = MovieScreeningFactory.create()
        new_seat = SeatFactory.create()
        new_data = {
            "movie_screening": new_screening.id,
            "seat": new_seat.id,
            "price": ticket.price + 5,
        }

        response = client.put(url, data=new_data, content_type="application/json")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["movie_screening"] == new_data["movie_screening"]
        assert response_data["seat"] == new_data["seat"]
        assert response_data["price"] == new_data["price"]

    def test_ticket_delete(self, client):
        ticket = TicketFactory.create()
        url = reverse("ticket-detail", args=[ticket.id])

        response = client.delete(url)

        assert response.status_code == 204
        assert not Ticket.objects.filter(id=ticket.id).exists()
