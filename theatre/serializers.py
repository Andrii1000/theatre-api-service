from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Play,
    Performance,
    Reservation,
    TheatreHall,
    Ticket
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )


class PlayListSerializer(PlaySerializer):
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    description = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )

    def get_description(self, obj):
        return f"{obj.description[:35]}..."


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name",
        read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity",
        read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "theatre_hall_name",
            "theatre_hall_capacity"
        )


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(
        many=False,
        read_only=True,
    )
    theatre_hall = TheatreHallSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play",
            "theatre_hall",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")
