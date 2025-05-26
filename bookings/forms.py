# bookings/forms.py

from django import forms
from .models import Booking, Contact
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'age', 'date']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def clean_email(self):
        email = self.cleaned_data['email']

        # 🚫 Disallow commas, semicolons, or spaces (to block multiple emails)
        if any(c in email for c in [',', ';', ' ']):
            raise ValidationError("Please enter only one valid email address.")

        # ✅ Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")

        return email
