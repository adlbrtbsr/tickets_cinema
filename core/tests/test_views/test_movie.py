import pytest
from django.urls import reverse

from core.models import Movie
from core.serializers import MovieSerializer
from core.tests.factories import ActorFactory, GenreFactory, MovieFactory

pytestmark = pytest.mark.django_db
movie_list_url = reverse("movie-list")


def test_movie_serialization(client):
    genre = GenreFactory()
    actor = ActorFactory()
    movie = MovieFactory(title="Test Movie", duration=120)
    movie.genres.add(genre)
    movie.actors.add(actor)
    url = reverse("movie-detail", args=[movie.id])
    expected_data = MovieSerializer(movie).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_movie_post(client):
    genre = GenreFactory()
    actor = ActorFactory()
    data = {
        "title": "Test Movie",
        "duration": 120,
        "genres": [genre.id],
        "actors": [actor.id],
    }

    response = client.post(movie_list_url, data=data, content_type="application/json")

    assert response.status_code == 201
    assert Movie.objects.filter(id=response.data["id"]).exists()


def test_movie_post_blank(client):
    response = client.post(movie_list_url, data={}, content_type="application/json")
    response_data = response.json()

    assert response.status_code == 400
    assert "title" in response_data
    assert "duration" in response_data


def test_movie_get_list(client):
    MovieFactory()
    MovieFactory()

    response = client.get(movie_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_movie_get_detail(client):
    movie = MovieFactory()
    url = reverse("movie-detail", args=[movie.id])

    response = client.get(url)

    assert response.status_code == 200


def test_movie_put(client):
    movie = MovieFactory()
    url = reverse("movie-detail", args=[movie.id])
    genre = GenreFactory()
    actor = ActorFactory()
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


def test_movie_delete(client):
    movie = MovieFactory()
    url = reverse("movie-detail", args=[movie.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Movie.objects.filter(id=movie.id).exists() is False
