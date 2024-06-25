from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('home.html', views.home, name="home"),
    path('contact.html', views.contact, name="contact"),
    path('about.html', views.about, name="about"),
    path('courses.html', views.courses, name="courses"),
    path('appointment.html', views.appointment, name="appointment"),
]