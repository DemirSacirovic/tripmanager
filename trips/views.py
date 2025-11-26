import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Trip


def trip_list(request):
    """
    GET /trips/ - Vraca listu svih trips kao json"""

    trips = Trip.objects.all()

    data = []
    for trip in trips:
        data.append(
            {
                "id": trip.id,
                "title": trip.title,
                "destination": trip.destination,
                "status": trip.status,
                "duration_days": trip.duration_days,
            }
        )

    return JsonResponse(data, safe=False)


class TripDetailView(View):
    """
    GET /trips/id/ - jedan trip"""

    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        data = {
            "id": trip.id,
            "title": trip.title,
            "destination": trip.destination,
            "status": trip.status,
            "start_date": str(trip.start_date),
            "end_date": str(trip.end_date),
            "duration_days": trip.duration_days,
        }

        return JsonResponse(data)


class TripListView(View):
    def get(self, request):
        trips = Trip.objects.select_related("traveler").all()

        data = []
        for trip in trips:
            data.append(
                {
                    "id": trip.id,
                    "title": trip.title,
                    "destination": trip.destination,
                    "status": trip.status,
                    "traveler": trip.traveler.full_name,
                }
            )

        return JsonResponse(data, safe=False)

    def post(self, request):
        """POST /trips/v2/ - kreiraj novi trip"""
        data = json.loads(request.body)

        trip = Trip.objects.create(
            title=data["title"],
            destination=data["destination"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            status=data["status"],
            traveler_id=1,
        )

        return JsonResponse({"id": trip.id, "title": trip.title, "message": "Trip created successfully"}, status=201)


class TripCreateView(View):
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        data = {
            "id": trip.id,
            "title": trip.title,
            "destination": trip.destination,
            "status": trip.status,
            "duration_days": trip.duration_days,
        }
        return JsonResponse(data)
