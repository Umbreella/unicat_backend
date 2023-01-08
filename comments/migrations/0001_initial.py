# Generated by Django 4.1.2 on 2022-12-25 09:26

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateField(default=datetime.datetime.now)),
                ('count_like', models.PositiveSmallIntegerField(default=0)),
                ('commented_type', models.CharField(choices=[('course', 'Курс'), ('news', 'Новость'), ('event', 'Мероприятие')], max_length=128)),
                ('commented_id', models.PositiveBigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['commented_type', 'commented_id'], name='comments_co_comment_c2e5f0_idx'),
        ),
    ]
