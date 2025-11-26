from django.db import models


class Traveler(models.Model):
    """
    Osoba koja putuje
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Trip(models.Model):
    """
    Business trip
    models.Model
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("approved", "Approved"),
    ]

    title = models.CharField(max_length=200)
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name="trips")

    destination = models.CharField(max_length=100)

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")  # Create your models here.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.destination}"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days
