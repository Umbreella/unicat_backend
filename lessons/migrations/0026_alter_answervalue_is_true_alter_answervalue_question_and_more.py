# Generated by Django 4.1.2 on 2023-05-18 17:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0037_remove_course_discount_alter_category_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0025_alter_userlesson_completed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answervalue',
            name='is_true',
            field=models.BooleanField(default=False, help_text='Is this answer correct or not.'),
        ),
        migrations.AlterField(
            model_name='answervalue',
            name='question',
            field=models.ForeignKey(help_text='The question to which this answer was created.', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='lessons.question'),
        ),
        migrations.AlterField(
            model_name='answervalue',
            name='value',
            field=models.CharField(help_text='Answer body.', max_length=128),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='count_questions',
            field=models.PositiveSmallIntegerField(default=0, help_text='The number of questions in the test, calculated automatically.'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(help_text='The course that the lesson belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.CharField(default='', help_text='A brief description of the lesson, which is displayed in the course content tab.', max_length=255),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Тема'), (2, 'Теория'), (3, 'Тест')], help_text='Type of lesson.'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='listeners',
            field=models.ManyToManyField(help_text='All users who have access to the lesson.', related_name='my_lessons', through='lessons.UserLesson', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, help_text='Parent lesson in relation to the current.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='serial_number',
            field=models.PositiveSmallIntegerField(default=1, help_text='Sequence number of the lesson.'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_limit',
            field=models.DurationField(blank=True, default=None, help_text='time limit for tests, if necessary.', null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(default='', help_text='Lesson name.', max_length=255),
        ),
        migrations.AlterField(
            model_name='lessonbody',
            name='body',
            field=models.TextField(help_text='Full content of the lesson.'),
        ),
        migrations.AlterField(
            model_name='lessonbody',
            name='lesson',
            field=models.OneToOneField(help_text='The lesson to which the full content refers.', on_delete=django.db.models.deletion.CASCADE, related_name='lesson_body', to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='question',
            name='body',
            field=models.CharField(help_text='Question body.', max_length=512),
        ),
        migrations.AlterField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(help_text='The lesson to which this question relates.', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Один вариант'), (2, 'Несколько вариантов'), (3, 'Свободный ответ')], help_text='Question type by the number of correct answers.'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='is_true',
            field=models.BooleanField(default=False, help_text='Is this answer correct.'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(help_text='The question to which this answer refers.', on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='lessons.question'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='user_attempt',
            field=models.ForeignKey(help_text='The user attempt to which this response refers.', on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='lessons.userattempt'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='count_true_answer',
            field=models.PositiveSmallIntegerField(default=0, help_text='The number of correct answers.'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='time_end',
            field=models.DateTimeField(blank=True, default=None, help_text='Attempt completion time.', null=True),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='time_start',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Attempt start time.'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='user_lesson',
            field=models.ForeignKey(help_text='The user lesson to which the attempt is attached.', on_delete=django.db.models.deletion.CASCADE, to='lessons.userlesson'),
        ),
        migrations.AlterField(
            model_name='userlesson',
            name='completed_at',
            field=models.DateField(blank=True, default=None, help_text='Has the lesson been completed by the user.', null=True),
        ),
        migrations.AlterField(
            model_name='userlesson',
            name='lesson',
            field=models.ForeignKey(help_text='A lesson that the user has access to.', on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='lessons.lesson'),
        ),
        migrations.AlterField(
            model_name='userlesson',
            name='user',
            field=models.ForeignKey(help_text='The user who got access to the lesson.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]