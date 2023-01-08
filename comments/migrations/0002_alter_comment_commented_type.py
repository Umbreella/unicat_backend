# Generated by Django 4.1.2 on 2022-12-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commented_type',
            field=models.CharField(choices=[('course', 'Курс'), ('news', 'Новость'), ('event', 'Мероприятие')], max_length=32),
        ),
    ]