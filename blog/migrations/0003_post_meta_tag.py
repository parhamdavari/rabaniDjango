# Generated by Django 4.1.13 on 2024-07-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_title_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_tag',
            field=models.CharField(default='Cosmetic Dentistry Content by Dr. Hossein Rabbani', max_length=255),
        ),
    ]
