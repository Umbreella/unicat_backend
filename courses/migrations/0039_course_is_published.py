# Generated by Django 4.1.2 on 2023-07-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0038_course_count_listeners'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Course is published.'),
        ),
    ]