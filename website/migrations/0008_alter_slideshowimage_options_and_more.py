# Generated by Django 4.2.13 on 2024-06-24 15:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_slideshowimagetranslation_delete_mymodel_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slideshowimage',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='slideshowimagetranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'slide show image Translation'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='has_btn',
        ),
        migrations.RemoveField(
            model_name='course',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='course',
            name='link',
        ),
        migrations.RemoveField(
            model_name='course',
            name='text',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title',
        ),
        migrations.RemoveField(
            model_name='courseimage',
            name='image',
        ),
        migrations.CreateModel(
            name='CourseTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('text', models.CharField(max_length=400, null=True, verbose_name='text')),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('link', models.CharField(default='#', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('has_btn', models.BooleanField(default=False)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='website.course')),
            ],
            options={
                'verbose_name': 'course Translation',
                'db_table': 'website_course_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='CourseImageTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('image', models.ImageField(upload_to='course_images/', verbose_name='image')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='website.courseimage')),
            ],
            options={
                'verbose_name': 'course image Translation',
                'db_table': 'website_courseimage_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
