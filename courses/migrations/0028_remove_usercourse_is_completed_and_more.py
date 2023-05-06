# Generated by Django 4.1.2 on 2023-02-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0027_alter_usercertificate_certificate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercourse',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='usercourse',
            name='when_completed',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]