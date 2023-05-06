# Generated by Django 4.1.2 on 2023-03-24 18:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0031_alter_coursebody_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercourse',
            old_name='when_completed',
            new_name='completed_at',
        ),
        migrations.AddField(
            model_name='usercourse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
