from datetime import date

from django.test import TestCase

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


# Create your tests here.
