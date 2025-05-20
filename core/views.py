from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response

from core.models import Actor, CinemaHall, Genre, Movie, MovieScreening, Seat, Ticket
from core.serializers import (
    ActorSerializer,
    CinemaHallSerializer,
    GenreSerializer,
    MovieScreeningSerializer,
    MovieSerializer,
    SeatSerializer,
    TicketSerializer,
)


class GenreViewSet(viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Genre created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Genre updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Genre deleted"}, status=204, content_type="application/json"
        )


class ActorViewSet(viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Actor created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Actor updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Actor deleted"}, status=204, content_type="application/json"
        )


class MovieApiView(generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Movie created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def get(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def put(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Movie updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Movie deleted"}, status=204, content_type="application/json"
        )


class CinemaHallApiView(generics.GenericAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Cinema Hall created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def get(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def put(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Cinema Hall updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Cinema Hall deleted"},
            status=204,
            content_type="application/json",
        )


class SeatApiView(generics.GenericAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Seat created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def get(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def put(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Seat updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Seat deleted"}, status=204, content_type="application/json"
        )


class MovieScreeningApiView(generics.GenericAPIView):
    queryset = MovieScreening.objects.all()
    serializer_class = MovieScreeningSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Movie screening created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def get(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def put(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Movie screening updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Movie screening deleted"},
            status=204,
            content_type="application/json",
        )


class TicketApiView(generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Ticket created", "data": serializer.data},
            status=201,
            content_type="application/json",
        )

    def get(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=200, content_type="application/json")

    def put(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"message": "Ticket updated", "data": serializer.data},
            status=200,
            content_type="application/json",
        )

    def delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return JsonResponse(
            {"message": "Ticket deleted"}, status=204, content_type="application/json"
        )
