from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Traveler, Trip
from .permissions import IsOwnerOrReadOnly
from .serializers import TravelerSerializer, TripSerializer
from .services import FlightService


class TravelerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing travelers.

    Provides CRUD operations for traveler records.
    """
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter travelers by department.
        """
        queryset = Traveler.objects.all()
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__icontains=department)
        return queryset


class TripViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing business trips.

    Provides CRUD operations plus approval workflow actions.
    Uses select_related to prevent N+1 queries on traveler lookups.
    """
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Returns trips with traveler data pre-fetched.
        Uses select_related to prevent N+1 query problem.
        """
        return Trip.objects.select_related('traveler').all()

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Approve a pending trip request.

        POST /api/trips/{id}/approve/
        """
        trip = self.get_object()
        if trip.status != "pending":
            return Response(
                {"error": "Only pending trips can be approved"},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip.status = "approved"
        trip.save()
        return Response({
            "status": "approved",
            "trip_id": trip.id,
            "message": f"Trip to {trip.destination} has been approved"
        })

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """
        Reject a pending trip request.

        POST /api/trips/{id}/reject/
        """
        trip = self.get_object()
        if trip.status != "pending":
            return Response(
                {"error": "Only pending trips can be rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip.status = "rejected"
        trip.save()
        return Response({
            "status": "rejected",
            "trip_id": trip.id,
            "message": f"Trip to {trip.destination} has been rejected"
        })

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """
        Submit a draft trip for approval.

        POST /api/trips/{id}/submit/
        """
        trip = self.get_object()
        if trip.status != "draft":
            return Response(
                {"error": "Only draft trips can be submitted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        trip.status = "pending"
        trip.save()
        return Response({
            "status": "pending",
            "trip_id": trip.id,
            "message": "Trip submitted for approval"
        })

    @action(detail=False, methods=["get"])
    def search_flights(self, request):
        """
        Search for available flights.

        GET /api/trips/search_flights/?origin=BEG&destination=BCN&date=2024-03-01
        """
        origin = request.query_params.get("origin", "BEG")
        destination = request.query_params.get("destination", "BCN")
        date = request.query_params.get("date", "2024-03-01")

        service = FlightService()
        flights = service.search_flights(origin, destination, date)

        if flights is None:
            return Response(
                {"error": "Flight search temporarily unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return Response(flights)
