# Generated by Django 4.1.2 on 2023-01-31 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0017_lesson_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='is_completed',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'theme'), (2, 'theory'), (3, 'test')]),
        ),
    ]
