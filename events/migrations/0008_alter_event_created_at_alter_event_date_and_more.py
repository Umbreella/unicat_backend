# Generated by Django 4.1.2 on 2023-05-18 17:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_alter_event_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Event creation time.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(help_text='Event date.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='Full description of the event.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(help_text='Event end time.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(default='', help_text='Venue of the event.', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='preview',
            field=models.ImageField(help_text='Event image.', upload_to='events/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='short_description',
            field=models.CharField(default='', help_text='A brief description of the event displayed on the icon.', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(help_text='Event start time.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(default='', help_text='Event name.', max_length=255),
        ),
        migrations.AlterField(
            model_name='new',
            name='author',
            field=models.ForeignKey(help_text='The user who created the news.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='new',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='News creation time.'),
        ),
        migrations.AlterField(
            model_name='new',
            name='description',
            field=models.TextField(help_text='Full description of the news.'),
        ),
        migrations.AlterField(
            model_name='new',
            name='preview',
            field=models.ImageField(help_text='News image.', upload_to='news/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='new',
            name='short_description',
            field=models.CharField(default='', help_text='A brief description of the news displayed on the icon.', max_length=255),
        ),
        migrations.AlterField(
            model_name='new',
            name='title',
            field=models.CharField(default='', help_text='News name.', max_length=255),
        ),
    ]
