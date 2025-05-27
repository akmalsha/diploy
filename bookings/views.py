from django.shortcuts import render, redirect
from django.http import JsonResponse
from bookings.models import Booking, Contact
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils import generate_invoice_pdf
from django.core.mail import EmailMessage, BadHeaderError
from .forms import ContactForm
from django.contrib import messages
from decimal import Decimal


def delete_all(request):
    Booking.objects.all().delete()
    return redirect('current_booking')


def currentbooking(request):
    all_bookings = Booking.objects.all().order_by('-id')  # newest first
    return render(request, 'bookings/current_booking.html', {'bookings': all_bookings})


def home(request):
    return render(request, 'home.html')


def success(request):
    booking = Booking.objects.latest('id')  # or however you're fetching it
    return render(request, 'success.html', {'booking': booking})


def thankyou(request):
    name = request.session.get('contact_name', 'Guest')
    email = request.session.get('contact_email', 'Not provided')
    message = request.session.get('contact_message', '')

    # Clear session data after use
    request.session.pop('contact_name', None)
    request.session.pop('contact_email', None)
    request.session.pop('contact_message', None)

    return render(request, 'thankyou.html', {
        'name': name,
        'email': email,
        'message': message,
    })


def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        date = request.POST.get('date')
        destination = request.POST.get('destination')
        people = request.POST.get('people')

        # Clean the price: remove ₹ and comma
        raw_price = request.POST.get('price', '0')
        cleaned_price = raw_price.replace('₹', '').replace(',', '').strip()
        try:
            price = Decimal(cleaned_price)
        except Exception as e:
            messages.error(request, f"Invalid price format: {raw_price}")
            return redirect('home')  # or render with error

        # Save the booking
        new_booking = Booking.objects.create(
            name=name,
            email=email,
            age=age,
            date=date,
            destination=destination,
            people=people,
            price=price
        )

        # Generate PDF
        context = {'booking': new_booking}
        pdf_content = generate_invoice_pdf('invoice.html', context)

        # Send booking confirmation email with PDF
        subject = 'Booking Confirmation with Invoice'
        message = f"""
Dear {name},

Thank you for your booking!

We have attached your booking invoice as a PDF.

Destination: {destination}
Date: {date}
People: {people}

Best regards,
Kerala Bliss Team
"""

        email_message = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        if pdf_content:
            email_message.attach('invoice.pdf', pdf_content, 'application/pdf')

        try:
            email_message.send(fail_silently=False)
        except Exception:
            messages.error(request, "Failed to send confirmation email. Please try again.")
            return redirect('home')

        return render(request, 'success.html', {'booking': new_booking})

    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            # Save the contact entry
            contact = Contact.objects.create(
                name=name,
                email=email,
                message=message_text
            )

            # Admin Email
            admin_subject = 'New Contact Form Submission'
            admin_body = f"""
Name: {name}
Email: {email}

Message:
{message_text}
"""
            admin_email = EmailMessage(
                subject=admin_subject,
                body=admin_body,
                from_email=settings.EMAIL_HOST_USER,
                to=['akmalshah410@gmail.com'],
            )

            # User Confirmation Email
            user_subject = 'Thank you for contacting us'
            user_body = f"""
Dear {name},

Thank you for reaching out to Kerala Bliss. We have received your message:

"{message_text}"

Our team will get back to you shortly.

Regards,  
Kerala Bliss Team
"""
            user_email = EmailMessage(
                subject=user_subject,
                body=user_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            try:
                admin_email.send(fail_silently=False)
                user_email.send(fail_silently=False)
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
                return redirect('contact')
            except Exception:
                messages.error(request, "Error sending email. Please try again later.")
                return redirect('contact')

            # Save data to session for thank you page
            request.session['contact_name'] = name
            request.session['contact_email'] = email
            request.session['contact_message'] = message_text

            return redirect('thankyou')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
