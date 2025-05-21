from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from core.views import (
    ActorViewSet,
    CinemaHallApiView,
    GenreViewSet,
    MovieApiView,
    MovieScreeningApiView,
    SeatApiView,
    TicketApiView,
)
from tickets.settings.local import DEBUG

router = DefaultRouter()
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"actors", ActorViewSet, basename="actor")


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("movies/<int:pk>/", MovieApiView.as_view(), name="movie-detail"),
    path("movies/", MovieApiView.as_view(), name="movie-list"),
    path(
        "cinema-halls/<int:pk>/", CinemaHallApiView.as_view(), name="cinema-hall-detail"
    ),
    path("cinema-halls/", CinemaHallApiView.as_view(), name="cinema-hall-list"),
    path("seats/<int:pk>/", SeatApiView.as_view(), name="seat-detail"),
    path("seats/", SeatApiView.as_view(), name="seat-list"),
    path(
        "screenings/<int:pk>/", MovieScreeningApiView.as_view(), name="screening-detail"
    ),
    path("screenings/", MovieScreeningApiView.as_view(), name="screening-list"),
    path("tickets/<int:pk>/", TicketApiView.as_view(), name="ticket-detail"),
    path("tickets/", TicketApiView.as_view(), name="ticket-list"),
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
