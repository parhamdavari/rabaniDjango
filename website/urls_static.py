"""
URL patterns for static site generation.

These patterns map to the static views and are used
during the static site build process.
"""

from django.urls import path
from . import views_static

urlpatterns = [
    path('', views_static.home, name='home'),
    path('home.html', views_static.home, name='home_html'),
    path('contact.html', views_static.contact, name='contact'),
    path('about.html', views_static.about, name='about'),
    path('courses.html', views_static.courses, name='courses'),
    path('appointment.html', views_static.appointment, name='appointment'),
]
