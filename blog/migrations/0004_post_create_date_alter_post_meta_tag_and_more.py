# Generated by Django 4.1.13 on 2024-07-11 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_meta_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='meta_tag',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_tag',
            field=models.CharField(max_length=255),
        ),
    ]
