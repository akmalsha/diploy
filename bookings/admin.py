from django.contrib import admin
from bookings.models import Booking, Contact

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'date')  # Display these columns in the admin list view
    search_fields = ('name', 'email')               # Adds search functionality

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')                # Display name and email
    search_fields = ('name', 'email')               # Search by name and email
