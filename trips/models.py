from django.db import models


class Traveler(models.Model):
    """
    Represents a person who travels for business.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Trip(models.Model):
    """
    Represents a business trip with approval workflow.
    """
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=200)
    traveler = models.ForeignKey(
        Traveler,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.destination}"

    @property
    def duration_days(self):
        """Calculate trip duration in days."""
        return (self.end_date - self.start_date).days

    @property
    def is_editable(self):
        """Trip can only be edited if not yet approved."""
        return self.status in ('draft', 'rejected')
