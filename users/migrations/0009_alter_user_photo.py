# Generated by Django 4.1.2 on 2022-12-27 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_teacher_photo_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='teachers/%Y/%m/%d/'),
        ),
    ]
