from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from core.models import MovieScreening
from core.serializers import MovieScreeningSerializer
from core.tests.factories import CinemaHallFactory, MovieFactory, MovieScreeningFactory

pytestmark = pytest.mark.django_db
screening_list_url = reverse("screening-list")


def test_movie_screening_serialization(client):
    hall = CinemaHallFactory()
    movie = MovieFactory()
    movie_screening = MovieScreeningFactory(movie=movie, hall=hall, date=timezone.now())
    url = reverse("screening-detail", args=[movie_screening.id])
    expected_data = MovieScreeningSerializer(movie_screening).data

    response = client.get(url)
    response_data = response.data

    assert response.status_code == 200
    assert response_data == expected_data


def test_movie_screening_post(client):
    movie = MovieFactory()
    hall = CinemaHallFactory()
    screening_date = (timezone.now() + timedelta(days=1)).isoformat()
    data = {
        "movie": movie.id,
        "date": screening_date,
        "hall": hall.id,
    }

    response = client.post(
        screening_list_url, data=data, content_type="application/json"
    )

    assert response.status_code == 201
    assert MovieScreening.objects.filter(id=response.data["id"]).exists()


def test_movie_screening_post_blank(client):
    expected = {
        "movie": ["This field is required."],
        "date": ["This field is required."],
        "hall": ["This field is required."],
    }

    response = client.post(screening_list_url, data={}, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == expected


def test_movie_screening_get_list(client):
    MovieScreeningFactory()
    MovieScreeningFactory()

    response = client.get(screening_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_movie_screening_get_detail(client):
    screening = MovieScreeningFactory()
    url = reverse("screening-detail", args=[screening.id])

    response = client.get(url)

    assert response.status_code == 200


def test_movie_screening_put(client):
    screening = MovieScreeningFactory()
    url = reverse("screening-detail", args=[screening.id])
    new_movie = MovieFactory()
    new_hall = CinemaHallFactory()
    new_date = (timezone.now() + timedelta(days=2)).isoformat()
    new_data = {"movie": new_movie.id, "date": new_date, "hall": new_hall.id}

    response = client.put(url, data=new_data, content_type="application/json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["movie"] == new_data["movie"]
    assert response_data["hall"] == new_data["hall"]


def test_movie_screening_delete(client):
    screening = MovieScreeningFactory()
    url = reverse("screening-detail", args=[screening.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert MovieScreening.objects.filter(id=screening.id).exists() is False
