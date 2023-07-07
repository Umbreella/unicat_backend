# Generated by Django 4.1.2 on 2023-05-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0037_remove_course_discount_alter_category_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='count_listeners',
            field=models.PositiveSmallIntegerField(default=0, help_text='Count listeners in course, calculated automatically.'),
        ),
    ]