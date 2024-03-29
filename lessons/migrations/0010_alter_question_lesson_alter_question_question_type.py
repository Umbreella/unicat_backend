# Generated by Django 4.1.2 on 2023-01-18 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_alter_lessonbody_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Один вариант'), (2, 'Несколько вариантов'), (3, 'Свободный ответ')]),
        ),
    ]
