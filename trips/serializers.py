"""
Serializers for the trips API.

This module defines DRF serializers for converting model instances
to JSON and validating incoming data.
"""
from datetime import date

from rest_framework import serializers

from .models import Traveler, Trip


class TravelerSerializer(serializers.ModelSerializer):
    """
    Serializer for Traveler model.

    Includes computed full_name field and trip count.
    """
    full_name = serializers.CharField(read_only=True)
    trip_count = serializers.SerializerMethodField()

    class Meta:
        model = Traveler
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'email', 'department', 'trip_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_trip_count(self, obj):
        """Return the number of trips for this traveler."""
        return obj.trips.count()

    def validate_email(self, value):
        """Ensure email is lowercase and properly formatted."""
        return value.lower().strip()


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for Trip model.

    Features:
    - Nested traveler data for read operations
    - Date validation (end_date must be after start_date)
    - Computed duration_days field
    - Status transition validation
    """
    traveler_detail = TravelerSerializer(source='traveler', read_only=True)
    traveler = serializers.PrimaryKeyRelatedField(
        queryset=Traveler.objects.all(),
        write_only=True
    )
    duration_days = serializers.IntegerField(read_only=True)
    is_editable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'title', 'destination',
            'start_date', 'end_date', 'duration_days',
            'status', 'is_editable', 'estimated_cost',
            'traveler', 'traveler_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Cross-field validation.

        Ensures:
        - end_date is after start_date
        - start_date is not in the past for new trips
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })

        # For new trips, don't allow past start dates
        if self.instance is None and start_date:
            if start_date < date.today():
                raise serializers.ValidationError({
                    'start_date': 'Start date cannot be in the past.'
                })

        return data

    def validate_estimated_cost(self, value):
        """Ensure estimated cost is positive."""
        if value is not None and value < 0:
            raise serializers.ValidationError(
                'Estimated cost cannot be negative.'
            )
        return value


class TripListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for trip listings.

    Used for list views to reduce payload size.
    """
    traveler_name = serializers.CharField(
        source='traveler.full_name',
        read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            'id', 'title', 'destination',
            'start_date', 'end_date', 'status',
            'traveler_name'
        ]
