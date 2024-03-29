# Generated by Django 4.1.2 on 2023-05-18 17:48

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import users.models.ChangeEmail
import users.models.ResetPassword


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_teacher_average_rating_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='average_rating',
            new_name='avg_rating',
        ),
        migrations.AlterField(
            model_name='changeemail',
            name='closed_at',
            field=models.DateTimeField(default=users.models.ChangeEmail.add_ten_minutes, help_text='Duration of the change request.'),
        ),
        migrations.AlterField(
            model_name='changeemail',
            name='email',
            field=models.EmailField(help_text='New user mail.', max_length=128),
        ),
        migrations.AlterField(
            model_name='changeemail',
            name='url',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='A unique link to confirm the shift.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='changeemail',
            name='user',
            field=models.ForeignKey(help_text='The user who requested the email change.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resetpassword',
            name='closed_at',
            field=models.DateTimeField(default=users.models.ResetPassword.add_ten_minutes, help_text='Duration of the change request.'),
        ),
        migrations.AlterField(
            model_name='resetpassword',
            name='url',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='A unique link to change your password.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='resetpassword',
            name='user',
            field=models.ForeignKey(help_text='The user who requested a password change.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='count_reviews',
            field=models.PositiveIntegerField(default=0, help_text='The total number of all reviews left by users for all courses of this teacher.'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='facebook',
            field=models.CharField(blank=True, default='', help_text='Link to the user`s Facebook page.', max_length=255),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='google_plus',
            field=models.CharField(blank=True, default='', help_text='Link to the user`s GooglePlus page.', max_length=255),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='twitter',
            field=models.CharField(blank=True, default='', help_text='Link to the user`s Twitter page.', max_length=255),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='vk',
            field=models.CharField(blank=True, default='', help_text='Link to the user`s VK page.', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='User`s unique email address.', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text='Username.', max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Is this account active.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Does the user have access to the administration panel.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='User`s last name.', max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='User password.', max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default=None, help_text='User Image.', null=True, upload_to='teachers/%Y/%m/%d/'),
        ),
    ]
