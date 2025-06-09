import pytest
from django.urls import reverse

from core.models import CinemaHall
from core.serializers import CinemaHallSerializer
from core.tests.factories import CinemaHallFactory

pytestmark = pytest.mark.django_db
cinema_hall_list_url = reverse("cinema-hall-list")


def test_cinema_hall_serialization(client):
    cinema_hall = CinemaHallFactory(name="Test Hall")
    url = reverse("cinema-hall-detail", args=[cinema_hall.id])
    expected_data = CinemaHallSerializer(cinema_hall).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_cinema_hall_post(client):
    hall = CinemaHallFactory.build()
    serialized = CinemaHallSerializer(hall).data

    response = client.post(
        cinema_hall_list_url, data=serialized, content_type="application/json"
    )

    assert response.status_code == 201
    assert CinemaHall.objects.filter(id=response.data["id"]).exists()


def test_cinema_hall_post_blank(client):
    response = client.post(
        cinema_hall_list_url, data={}, content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json() == {"name": ["This field is required."]}


def test_cinema_hall_get_list(client):
    CinemaHallFactory()
    CinemaHallFactory()

    response = client.get(cinema_hall_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_cinema_hall_get_detail(client):
    hall = CinemaHallFactory()
    url = reverse("cinema-hall-detail", args=[hall.id])

    response = client.get(url)

    assert response.status_code == 200


def test_cinema_hall_put(client):
    hall = CinemaHallFactory()
    url = reverse("cinema-hall-detail", args=[hall.id])
    new_data = {"name": "Updated Hall"}

    response = client.put(url, data=new_data, content_type="application/json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["name"] == new_data["name"]


def test_cinema_hall_delete(client):
    hall = CinemaHallFactory()
    url = reverse("cinema-hall-detail", args=[hall.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert CinemaHall.objects.filter(id=hall.id).exists() is False
