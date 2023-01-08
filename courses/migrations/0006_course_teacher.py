# Generated by Django 4.1.2 on 2022-11-20 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_teacher'),
        ('courses', '0005_alter_course_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.teacher'),
        ),
    ]