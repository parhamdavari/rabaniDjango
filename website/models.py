from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class SlideShowImage(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('title'), max_length=200, blank=True, null=False, default=" "),
        text = models.CharField(max_length=200, blank=True, null=False, default=" "),
        link = models.CharField(max_length=300, default='#'),
        has_btn = models.BooleanField(default=False),
        is_active = models.BooleanField(default=True),
        image = models.ImageField(upload_to='slideshow_images/'),
        created_date = models.DateField(default=timezone.now),
    )
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title



class GalleryImage(models.Model):
    text = models.CharField(max_length=200, blank=True, null=False, default=" ")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='gallery_images/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text

class PatientImage(models.Model):
    text = models.CharField(max_length=200, blank=True, null=False, default=" ")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='patient_images/')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text

    
class Course(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('title'), max_length=200),
        text = models.CharField(_('text'), max_length=400, blank=True, null=False, default=" "),
        created_date = models.DateField(default=timezone.now),
        link = models.CharField(max_length=100, default='#'),
        is_active = models.BooleanField(default=True),
        has_btn = models.BooleanField(default=False),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title




class CourseImage(TranslatableModel):
    course = models.ForeignKey(Course, related_name='images', on_delete=models.CASCADE)
    translations = TranslatedFields(
        image = models.ImageField(_('image'), upload_to='course_images/'),
    )
    