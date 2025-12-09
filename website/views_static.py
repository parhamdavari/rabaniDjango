"""
Static site views for generating static HTML pages.

These views are simplified versions without POST handling, email sending,
or session management. They are used only during static site generation.
"""

from django.shortcuts import render
from .models import SlideShowImage, PatientImage, GalleryImage, Course


def home(request):
    """Home page with slideshow, patient images, and gallery."""
    slideshow_images = SlideShowImage.objects.all()
    patient_images = PatientImage.objects.all()
    gallery_images = GalleryImage.objects.all()
    return render(request, 'templates_static/home.html', {
        'slideshow_images': slideshow_images,
        'patient_images': patient_images,
        'gallery_images': gallery_images
    })


def about(request):
    """About page - static content."""
    return render(request, 'templates_static/about.html', {})


def courses(request):
    """Courses page with course listings from database."""
    courses_list = Course.objects.all()
    return render(request, 'templates_static/courses.html', {'courses': courses_list})


def contact(request):
    """
    Contact page - form submission handled by FormSubmit.co.
    No POST handling needed for static site.
    """
    return render(request, 'templates_static/contact.html', {})


def appointment(request):
    """
    Appointment confirmation page.
    Shown after FormSubmit.co redirects back with success parameter.
    """
    return render(request, 'templates_static/appointment.html', {})
