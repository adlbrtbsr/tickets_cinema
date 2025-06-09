import pytest
from django.urls import reverse

from core.models import Actor
from core.serializers import ActorSerializer
from core.tests.factories import ActorFactory

pytestmark = pytest.mark.django_db
actor_list_url = reverse("actor-list")


def test_actor_serialization(client):
    actor = ActorFactory(name="Test Actor", age=27)
    url = reverse("actor-detail", args=[actor.id])
    expected_data = ActorSerializer(actor).data

    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == expected_data


def test_actor_post(client):
    actor = ActorFactory.build()
    serialized = ActorSerializer(actor).data

    response = client.post(
        actor_list_url, data=serialized, content_type="application/json"
    )

    assert response.status_code == 201
    assert Actor.objects.filter(id=response.data["id"]).exists()


def test_actor_post_blank(client):
    expected = {
        "name": ["This field is required."],
        "age": ["This field is required."],
        "nationality": ["This field is required."],
    }

    response = client.post(actor_list_url, data={}, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == expected


def test_actor_get_list(client):
    ActorFactory()
    ActorFactory()

    response = client.get(actor_list_url)
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2


def test_actor_get_detail(client):
    actor = ActorFactory()
    url = reverse("actor-detail", args=[actor.id])

    response = client.get(url)

    assert response.status_code == 200


def test_actor_put(client):
    actor = ActorFactory(age=26)
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


def test_actor_delete(client):
    actor = ActorFactory()
    url = reverse("actor-detail", args=[actor.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Actor.objects.filter(id=actor.id).exists() is False
