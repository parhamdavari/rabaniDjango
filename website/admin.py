from django.contrib import admin
from .models import SlideShowImage, PatientImage, GalleryImage, Course, CourseImage
from django.utils.html import format_html
from parler.admin import TranslatableAdmin, TranslatableTabularInline


class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
    image_tag.short_description = 'Image'
    list_display = ['image_tag']

admin.site.register(PatientImage, ImageAdmin)
admin.site.register(GalleryImage, ImageAdmin)
admin.site.register(SlideShowImage, TranslatableAdmin)


class ImageInline(TranslatableTabularInline):
    model = CourseImage
    extra = 1  # number of extra forms

class CourseAdmin(TranslatableAdmin):
    inlines = [ImageInline]

admin.site.register(Course, CourseAdmin)



