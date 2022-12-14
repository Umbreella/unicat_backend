# Generated by Django 4.1.2 on 2022-12-07 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='courses.course'),
        ),
        migrations.CreateModel(
            name='ShortLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(default='', max_length=8)),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='', max_length=512)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course')),
                ('parent_lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.shortlesson')),
            ],
        ),
    ]
