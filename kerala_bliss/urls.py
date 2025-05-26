from django.contrib import admin
from django.urls import path, include
from bookings import views as bookings_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bookings_views.home, name='home'),
    path('booking/', bookings_views.booking, name='booking'),
    path('contact/', bookings_views.contact, name='contact'),
    path('success/',bookings_views.success,name='success'),
    path('thankyou/', bookings_views.thankyou, name='thankyou'),
    path('current_booking/', bookings_views.currentbooking, name='current_booking'),
    path('delete_all/', bookings_views.delete_all, name='delete_all'),


]


