# Generated by Django 4.1.2 on 2023-01-31 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0016_alter_lesson_lesson_type_alter_lesson_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]