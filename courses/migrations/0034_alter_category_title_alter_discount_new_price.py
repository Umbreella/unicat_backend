# Generated by Django 4.1.2 on 2023-05-05 08:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_alter_course_count_independents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.RenameField(
            model_name='discount',
            old_name='new_price',
            new_name='percent',
        ),
        migrations.AlterField(
            model_name='discount',
            name='percent',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]