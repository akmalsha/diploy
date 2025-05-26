# bookings/models.py

from django.db import models


class Booking(models.Model):
    DESTINATIONS = [
        ('Munnar', 'Munnar'),
        ('Alleppey', 'Alleppey'),
        ('Wayanad', 'Wayanad'),
        # Add more if needed
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    date = models.DateField()
    destination = models.CharField(max_length=50, choices=DESTINATIONS, default='Munnar')
    people = models.PositiveIntegerField(default=1)
    banner = models.ImageField(default='fallback.png', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    


    def __str__(self):
        return f"Booking by {self.name} on {self.date} to {self.destination}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name}"
