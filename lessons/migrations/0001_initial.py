# Generated by Django 4.1.2 on 2023-01-12 08:35

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0022_usercertificate_usercourse_remove_course_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=128)),
                ('is_true', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.PositiveSmallIntegerField(default=1)),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=255)),
                ('lesson_type', models.CharField(choices=[('theory', 'Теория'), ('test', 'Тестирование')], max_length=6)),
                ('time_limit', models.DurationField(blank=True, default=None, null=True)),
                ('count_questions', models.PositiveSmallIntegerField(default=0)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=512)),
                ('question_type', models.CharField(choices=[('one', 'Один вариант'), ('many', 'Несколько вариантов'), ('free', 'Свободный ответ')], max_length=6)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='UserAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_end', models.DateTimeField(blank=True, default=None, null=True)),
                ('count_true_answer', models.PositiveSmallIntegerField(default=0)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_true', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.question')),
                ('user_attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.userattempt')),
            ],
        ),
        migrations.CreateModel(
            name='SelectedUserAnswerValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_answer', models.CharField(blank=True, max_length=128)),
                ('answer_value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.answervalue')),
                ('user_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.useranswer')),
            ],
        ),
        migrations.CreateModel(
            name='LessonBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='answervalue',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.question'),
        ),
    ]
