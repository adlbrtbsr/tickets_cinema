from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from core.views import (
    ActorViewSet,
    CinemaHallCreateView,
    CinemaHallDetailView,
    GenreViewSet,
    MovieCreateView,
    MovieDetailView,
    MovieScreeningCreateView,
    MovieScreeningDetailView,
    SeatCreateView,
    SeatDetailView,
    TicketCreateView,
    TicketDetailView,
)
from tickets.settings.local import DEBUG

router = DefaultRouter()
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"actors", ActorViewSet, basename="actor")


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("movies/", MovieCreateView.as_view(), name="movie-list"),
    path(
        "cinema-halls/<int:pk>/",
        CinemaHallDetailView.as_view(),
        name="cinema-hall-detail",
    ),
    path("cinema-halls/", CinemaHallCreateView.as_view(), name="cinema-hall-list"),
    path("seats/<int:pk>/", SeatDetailView.as_view(), name="seat-detail"),
    path("seats/", SeatCreateView.as_view(), name="seat-list"),
    path(
        "screenings/<int:pk>/",
        MovieScreeningDetailView.as_view(),
        name="screening-detail",
    ),
    path("screenings/", MovieScreeningCreateView.as_view(), name="screening-list"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("tickets/", TicketCreateView.as_view(), name="ticket-list"),
]

if DEBUG:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
    ]
