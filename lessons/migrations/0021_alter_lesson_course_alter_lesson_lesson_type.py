# Generated by Django 4.1.2 on 2023-03-21 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0031_alter_coursebody_course'),
        ('lessons', '0020_alter_lesson_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')]),
        ),
    ]
