# Generated by Django 4.1.2 on 2022-12-14 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_course_discount_alter_shortlesson_parent_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=7, null=True),
        ),
    ]
