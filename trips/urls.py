from django.urls import path

from . import views

urlpatterns = [
    path("", views.trip_list, name="trip-list"),
    path("v2/", views.TripListView.as_view(), name="trip-list-v2"),
    path("<int:trip_id>/", views.TripDetailView.as_view(), name="trip-detail"),
]
