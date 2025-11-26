from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Traveler, Trip
from .permissions import IsOwnerOrReadOnly
from .serializers import TravelerSerializer, TripSerializer
from .services import FlightService


class TravelerViewSet(viewsets.ModelViewSet):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    permission_classes = [IsAuthenticated]


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        trip = self.get_object()
        trip.status = "approved"
        trip.save()
        return Response({"status": "approved", "trip_id": trip.id})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        trip = self.get_object()
        trip.status = "rejected"
        trip.save()
        return Response({"status": "rejected", "trip_id": trip.id})

    @action(detail=False, methods=["get"])
    def search_flights(self, request):
        origin = request.query_params.get("origin", "BEG")
        destination = request.query_params.get("destination", "BER")
        date = request.query_params.get("date", "2024-03-01")
        service = FlightService()
        flights = service.search_flights(origin, destination, date)
        return Response(flights)
