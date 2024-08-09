from rest_framework import views, viewsets

from theatre.models import (
    Actor,
    Genre,
    Play,
    Performance,
    Reservation,
    TheatreHall,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TheatreHallSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceDetailSerializer,
    PerformanceListSerializer,
)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().select_related("play", "theatre_hall")

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play", "tickets__performance__theatre_hall"
    )
    serializer_class = ReservationSerializer

