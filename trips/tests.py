from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Traveler, Trip


class TravelerTestCase(TestCase):
    def setUp(self):
        self.traveler = Traveler.objects.create(
            first_name="John", last_name="Doe", email="john@example.com", department="IT"
        )

        self.trip = Trip.objects.create(
            title="Berlin Conference",
            destination="Berlin",
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 5),
            status="draft",
            traveler=self.traveler,
        )

    def test_trip_creation(self):
        self.assertEqual(self.trip.title, "Berlin Conference")
        self.assertEqual(self.trip.destination, "Berlin")

    def test_trip_duration(self):
        self.assertEqual(self.trip.duration_days, 4)

    def test_trip_str(self):
        self.assertIn("Berlin", str(self.trip))


class TripTestCase(APITestCase):
    """Test Trip API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.client.force_authenticate(user=self.user)

        self.traveler = Traveler.objects.create(
            first_name="Jane", last_name="Doe", email="jane@example.com", department="Sales"
        )

        self.trip = Trip.objects.create(
            title="Paris Meeting",
            destination="Paris",
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 5),
            status="pending",
            traveler=self.traveler,
        )

    def test_list_trips(self):
        response = self.client.get("/api/trips/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_approve_trip(self):
        response = self.client.post(f"/api/trips/{self.trip.id}/approve/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, "approved")

    def test_reject_trip(self):
        response = self.client.post(f"/api/trips/{self.trip.id}/reject/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, "rejected")
