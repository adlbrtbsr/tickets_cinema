import pytest
from django.urls import reverse

from core.models import Seat
from core.serializers import SeatSerializer
from core.tests.factories import CinemaHallFactory, SeatFactory

pytestmark = pytest.mark.django_db
seat_list_url = reverse("seat-list")


def test_seat_serialization(client):
    hall = CinemaHallFactory()
    seat = SeatFactory(row=1, number=2, hall=hall)
    url = reverse("seat-detail", args=[seat.id])
    expected_data = SeatSerializer(seat).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_seat_post(client):
    hall = CinemaHallFactory()
    seat = SeatFactory.build(hall=hall)
    serialized = SeatSerializer(seat).data

    response = client.post(
        seat_list_url, data=serialized, content_type="application/json"
    )

    assert response.status_code == 201
    assert Seat.objects.filter(id=response.data["id"]).exists()


def test_seat_post_blank(client):
    expected = {
        "row": ["This field is required."],
        "number": ["This field is required."],
        "hall": ["This field is required."],
    }

    response = client.post(seat_list_url, data={}, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == expected


def test_seat_get_list(client):
    SeatFactory()
    SeatFactory()

    response = client.get(seat_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_seat_get_detail(client):
    seat = SeatFactory()
    url = reverse("seat-detail", args=[seat.id])

    response = client.get(url)

    assert response.status_code == 200


def test_seat_put(client):
    seat = SeatFactory(row=1)
    url = reverse("seat-detail", args=[seat.id])
    new_data = {"row": seat.row + 1, "number": seat.number, "hall": seat.hall.id}

    response = client.put(url, data=new_data, content_type="application/json")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["row"] == new_data["row"]


def test_seat_delete(client):
    seat = SeatFactory()
    url = reverse("seat-detail", args=[seat.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Seat.objects.filter(id=seat.id).exists() is False
