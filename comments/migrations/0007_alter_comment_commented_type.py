# Generated by Django 4.1.2 on 2023-03-14 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_alter_comment_commented_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commented_type',
            field=models.CharField(choices=[(0, 'Курс'), (1, 'Новость'), (2, 'Мероприятие')], max_length=8),
        ),
    ]
