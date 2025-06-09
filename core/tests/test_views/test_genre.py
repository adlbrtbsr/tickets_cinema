import pytest
from django.urls import reverse

from core.models import Genre
from core.serializers import GenreSerializer
from core.tests.factories import GenreFactory

pytestmark = pytest.mark.django_db
genre_list_url = reverse("genre-list")


def test_genre_serialization(client):
    genre = GenreFactory(name="Test Genre", is_for_adults=True)
    url = reverse("genre-detail", args=[genre.id])
    expected_data = GenreSerializer(genre).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_genre_post(client):
    genre = GenreFactory.build()
    serialized = GenreSerializer(genre).data

    response = client.post(
        genre_list_url, data=serialized, content_type="application/json"
    )

    assert response.status_code == 201
    assert Genre.objects.filter(id=response.data["id"]).exists()


def test_genre_post_blank(client):
    response = client.post(genre_list_url, data={}, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {"name": ["This field is required."]}


def test_genre_get_list(client):
    GenreFactory()
    GenreFactory()

    response = client.get(genre_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_genre_get_detail(client):
    genre = GenreFactory()
    url = reverse("genre-detail", args=[genre.id])

    response = client.get(url)

    assert response.status_code == 200


def test_genre_put(client):
    genre = GenreFactory()
    url = reverse("genre-detail", args=[genre.id])
    updated_data = {"name": "Updated Genre", "is_for_adults": True}

    response = client.put(url, data=updated_data, content_type="application/json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["name"] == updated_data["name"]
    assert response_data["is_for_adults"] == updated_data["is_for_adults"]


def test_genre_delete(client):
    genre = GenreFactory()
    url = reverse("genre-detail", args=[genre.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Genre.objects.filter(id=genre.id).exists() is False
