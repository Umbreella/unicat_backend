# Generated by Django 4.1.2 on 2023-02-28 09:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.ImageField(upload_to='resources/%Y/%m/%d/')),
                ('loaded_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
