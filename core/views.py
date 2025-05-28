from rest_framework import generics, viewsets

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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CinemaHallCreateView(generics.ListCreateAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class CinemaHallDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class SeatCreateView(generics.ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class SeatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class MovieScreeningCreateView(generics.ListCreateAPIView):
    queryset = MovieScreening.objects.all()
    serializer_class = MovieScreeningSerializer


class MovieScreeningDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieScreening.objects.all()
    serializer_class = MovieScreeningSerializer


class TicketCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
