from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    PerformanceViewSet,
    TheatreHallViewSet,
    ReservationViewSet
)


router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls)),]

app_name = "theatre"
