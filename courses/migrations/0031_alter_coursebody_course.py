# Generated by Django 4.1.2 on 2023-02-27 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_rename_lesson_completed_usercourse_count_independents_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursebody',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_body', to='courses.course'),
        ),
    ]
