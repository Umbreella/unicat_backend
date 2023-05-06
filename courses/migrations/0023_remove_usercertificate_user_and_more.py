# Generated by Django 4.1.2 on 2023-01-12 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_usercertificate_usercourse_remove_course_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercertificate',
            name='user',
        ),
        migrations.AlterField(
            model_name='usercertificate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.usercourse'),
        ),
    ]
