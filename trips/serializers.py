from rest_framework import serializers

from .models import Traveler, Trip


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = ["id", "first_name", "last_name", "email", "department"]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ["id", "title", "start_date", "end_date", "destination", "status", "duration_days", "traveler"]
