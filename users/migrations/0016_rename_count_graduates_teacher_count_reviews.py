# Generated by Django 4.1.2 on 2023-05-14 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_teacher_personal_signature'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='count_graduates',
            new_name='count_reviews',
        ),
    ]