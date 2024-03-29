# Generated by Django 4.1.2 on 2023-01-30 18:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0026_coursebody'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercertificate',
            name='certificate',
            field=models.FileField(blank=True, default=None, null=True, upload_to='certificates/docs/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='usercertificate',
            name='preview',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='certificates/preview/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_course_progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usercourse',
            unique_together={('course', 'user')},
        ),
    ]
