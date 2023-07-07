# Generated by Django 4.1.2 on 2023-05-18 17:48

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_rename_average_rating_teacher_avg_rating_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0036_remove_coursestat_avg_rating_course_avg_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='discount',
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(help_text='Category name.', max_length=128),
        ),
        migrations.AlterField(
            model_name='course',
            name='avg_rating',
            field=models.DecimalField(decimal_places=1, default=0, help_text='Average rating based on comments, calculated automatically.', max_digits=2),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(help_text='Course category.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.category'),
        ),
        migrations.AlterField(
            model_name='course',
            name='count_independents',
            field=models.PositiveSmallIntegerField(default=0, help_text='Count independents in course, calculated automatically.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='count_lectures',
            field=models.PositiveSmallIntegerField(default=0, help_text='Count lectures in course, calculated automatically.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Course creation time.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='listeners',
            field=models.ManyToManyField(help_text='All students of the course.', related_name='my_courses', through='courses.UserCourse', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='preview',
            field=models.ImageField(help_text='Course picture.', upload_to='courses/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Course price.', max_digits=7),
        ),
        migrations.AlterField(
            model_name='course',
            name='short_description',
            field=models.CharField(default='', help_text='A few words about the course, shown on the course icon.', max_length=255),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(help_text='The teacher who leads the course.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.teacher'),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(default='', help_text='Course name.', max_length=128),
        ),
        migrations.AlterField(
            model_name='coursebody',
            name='body',
            field=models.TextField(help_text='Course content displayed on the Description tab.'),
        ),
        migrations.AlterField(
            model_name='coursebody',
            name='course',
            field=models.OneToOneField(help_text='The course for which you need to create its content.', on_delete=django.db.models.deletion.CASCADE, related_name='course_body', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_comments',
            field=models.PositiveIntegerField(default=0, help_text='Total number of all comments.'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_five_rating',
            field=models.PositiveIntegerField(default=0, help_text='Number of comments with a rating of 5, calculated at the time of creating a comment to the course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_four_rating',
            field=models.PositiveIntegerField(default=0, help_text='Number of comments with a rating of 4, calculated at the time of creating a comment to the course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_one_rating',
            field=models.PositiveIntegerField(default=0, help_text='Number of comments with a rating of 1, calculated at the time of creating a comment to the course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_three_rating',
            field=models.PositiveIntegerField(default=0, help_text='Number of comments with a rating of 3, calculated at the time of creating a comment to the course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='count_two_rating',
            field=models.PositiveIntegerField(default=0, help_text='Number of comments with a rating of 2, calculated at the time of creating a comment to the course'),
        ),
        migrations.AlterField(
            model_name='coursestat',
            name='course',
            field=models.OneToOneField(help_text='The course for which statistics are collected.', on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='course',
            field=models.ForeignKey(help_text='The course for which the discount was created.', on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='end_date',
            field=models.DateTimeField(help_text='Discount end date.'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='percent',
            field=models.IntegerField(help_text='Discount percentage, from 0 to 100.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start_date',
            field=models.DateTimeField(help_text='Discount start date.'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, help_text='Have you completed enough lessons to consider the course completed at a minimum', null=True),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='count_independents_completed',
            field=models.PositiveSmallIntegerField(default=0, help_text='The number of independent tasks performed by the user from the course, calculated automatically.'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='count_lectures_completed',
            field=models.PositiveSmallIntegerField(default=0, help_text='The number of lectures delivered by the user from the course, calculated automatically.'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='course',
            field=models.ForeignKey(help_text='The course that has been accessed.', on_delete=django.db.models.deletion.CASCADE, related_name='user_courses', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Access creation time.'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='last_view',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The date of the last viewing of the lesson from the course.'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(help_text='The user who gained access.', on_delete=django.db.models.deletion.CASCADE, related_name='my_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]