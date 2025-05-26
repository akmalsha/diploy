# bookings/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success_view, name='success'),
    path('thankyou/',views.thankyou,name='thankyou'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('current_booking/', views.current_booking, name='current_booking'),
    path('delete_all/', views.delete_all, name='delete_all'),
   

    
]
