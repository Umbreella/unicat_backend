# Generated by Django 4.1.2 on 2023-01-18 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_alter_question_lesson_alter_question_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answervalue',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='lessons.question'),
        ),
    ]