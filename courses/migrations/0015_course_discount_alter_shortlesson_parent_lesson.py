# Generated by Django 4.1.2 on 2022-12-09 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_remove_shortlesson_custom_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='shortlesson',
            name='parent_lesson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childs', to='courses.shortlesson'),
        ),
    ]