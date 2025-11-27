"""
Django Admin configuration for the trips application.

This module customizes the Django Admin interface for managing
Travelers and Trips, providing efficient list views, filtering,
and search capabilities.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Traveler, Trip


@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    """
    Admin configuration for Traveler model.

    Features:
    - Searchable by name and email
    - Filterable by department
    - Displays trip count for each traveler
    """

    list_display = ["full_name", "email", "department", "trip_count", "created_at"]
    list_filter = ["department", "created_at"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ["last_name", "first_name"]

    readonly_fields = ["created_at"]

    fieldsets = (
        ("Personal Information", {"fields": ("first_name", "last_name", "email")}),
        ("Work Information", {"fields": ("department",)}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def trip_count(self, obj):
        """Display the number of trips for this traveler."""
        return obj.trips.count()

    trip_count.short_description = "Trips"

    def full_name(self, obj):
        """Display full name as a single column."""
        return obj.full_name

    full_name.short_description = "Name"
    full_name.admin_order_field = "last_name"


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Admin configuration for Trip model.

    Features:
    - Color-coded status display
    - Quick filters for status and dates
    - Inline editing of common fields
    - Custom actions for bulk approval/rejection
    """

    list_display = [
        "title",
        "traveler",
        "destination",
        "start_date",
        "end_date",
        "status_badge",
        "estimated_cost",
        "created_at",
    ]
    list_filter = ["status", "start_date", "destination"]
    search_fields = ["title", "destination", "traveler__first_name", "traveler__last_name"]
    date_hierarchy = "start_date"
    ordering = ["-created_at"]

    readonly_fields = ["created_at", "updated_at", "duration_display"]

    list_select_related = ["traveler"]

    fieldsets = (
        ("Trip Details", {"fields": ("title", "destination", "traveler")}),
        ("Dates", {"fields": ("start_date", "end_date", "duration_display")}),
        ("Status & Cost", {"fields": ("status", "estimated_cost")}),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    actions = ["approve_trips", "reject_trips"]

    def status_badge(self, obj):
        """Display status as a colored badge."""
        colors = {
            "draft": "#6c757d",
            "pending": "#ffc107",
            "approved": "#28a745",
            "rejected": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"

    def duration_display(self, obj):
        """Display calculated trip duration."""
        return f"{obj.duration_days} days"

    duration_display.short_description = "Duration"

    @admin.action(description="Approve selected trips")
    def approve_trips(self, request, queryset):
        """Bulk approve pending trips."""
        updated = queryset.filter(status="pending").update(status="approved")
        self.message_user(request, f"{updated} trip(s) approved.")

    @admin.action(description="Reject selected trips")
    def reject_trips(self, request, queryset):
        """Bulk reject pending trips."""
        updated = queryset.filter(status="pending").update(status="rejected")
        self.message_user(request, f"{updated} trip(s) rejected.")
