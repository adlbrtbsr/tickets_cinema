import pytest
from django.urls import reverse

from core.models import Ticket
from core.serializers import TicketSerializer
from core.tests.factories import MovieScreeningFactory, SeatFactory, TicketFactory

pytestmark = pytest.mark.django_db
ticket_list_url = reverse("ticket-list")


def test_ticket_serialization(client):
    movie_screening = MovieScreeningFactory()
    seat = SeatFactory()
    ticket = TicketFactory(movie_screening=movie_screening, seat=seat, price=21)
    url = reverse("ticket-detail", args=[ticket.id])
    expected_data = TicketSerializer(ticket).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_ticket_post(client):
    screening = MovieScreeningFactory()
    seat = SeatFactory()
    data = {"movie_screening": screening.id, "seat": seat.id, "price": 20}

    response = client.post(ticket_list_url, data=data, content_type="application/json")

    assert response.status_code == 201
    assert Ticket.objects.filter(id=response.data["id"]).exists()


def test_ticket_post_blank(client):
    expected = {
        "movie_screening": ["This field is required."],
        "price": ["This field is required."],
    }

    response = client.post(ticket_list_url, data={}, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == expected


def test_ticket_get_list(client):
    TicketFactory()
    TicketFactory()

    response = client.get(ticket_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_ticket_get_detail(client):
    ticket = TicketFactory()
    url = reverse("ticket-detail", args=[ticket.id])

    response = client.get(url)

    assert response.status_code == 200


def test_ticket_put(client):
    ticket = TicketFactory()
    url = reverse("ticket-detail", args=[ticket.id])
    new_screening = MovieScreeningFactory()
    new_seat = SeatFactory()
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


def test_ticket_delete(client):
    ticket = TicketFactory()
    url = reverse("ticket-detail", args=[ticket.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Ticket.objects.filter(id=ticket.id).exists() is False
