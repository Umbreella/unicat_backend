# Generated by Django 4.1.2 on 2023-01-15 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_alter_lesson_lesson_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Теория'), (2, 'Тестирование')]),
        ),
    ]