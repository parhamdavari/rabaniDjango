# Generated by Django 4.2.13 on 2024-06-20 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.CreateModel(
            name='CourseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='course_images/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.course')),
            ],
        ),
    ]
