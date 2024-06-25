from django.shortcuts import render
from django.core.mail import send_mail
from .models import SlideShowImage, PatientImage, GalleryImage, Course

# Create your views here.
def home(request):
    slideshow_images = SlideShowImage.objects.all()
    patient_images = PatientImage.objects.all()
    gallery_images = GalleryImage.objects.all()
    return render(request, 'home.html', 
                  {'slideshow_images': slideshow_images,
                   'patient_images': patient_images,
                   'gallery_images': gallery_images})

def about(request):
    return render(request, 'about.html', {})

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses':courses})

def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # Send an email
        if not request.session.get('mail_sent', False):
            send_mail(
                f"Message from {message_name}", # Subject
                message, # Message
                message_email, # From email
                ['plavigne19@gmail.com'],
                fail_silently=False,
            )
            request.session['mail_sent'] = True
            return render(request, 'contact.html', {'message_name':message_name})
        else:
            return render(request, 'contact.html', {'message_name':message_name})
    else:
        return render(request, 'contact.html', {})

def appointment(request):
    if request.method == 'POST':
        appointment_name = request.POST['appointment-name']
        appointment_email = request.POST['appointment-email']
        appointment_date = request.POST['appointment-date']
        appointment_time = request.POST['appointment-time']
        appointment_message = request.POST['appointment-message']
        email_content = f"Name: {appointment_name}\nEmail: {appointment_email}\nDate: {appointment_date}\nTime: {appointment_time}\nMessage: {appointment_message}"

        # Send an email
        # if not request.session.get('mail_sent', False):
        send_mail(
            f"Appointment Request by {appointment_name}", # Subject
            email_content, # Message
            appointment_email, # From email
            ['plavigne19@gmail.com'], # To email
            fail_silently=False,
        )
            # request.session['mail_sent'] = True
        return render(request, 'appointment.html', {
            'appointment_name':appointment_name,
            'appointment_email':appointment_email,
            'appointment_date':appointment_date,
            'appointment_time':appointment_time,
            'appointment_message':appointment_message,})
        # else:
            # return render(request, 'contact.html', {'message-name':appointment_name})
    else:
        return render(request, 'home.html', {})