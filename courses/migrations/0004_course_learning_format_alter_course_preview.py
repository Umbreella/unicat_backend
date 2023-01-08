# Generated by Django 4.1.2 on 2022-11-19 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_learning_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='learning_format',
            field=models.CharField(choices=[('part', 'Дистанционно'), ('full', 'Очно'), ('both', 'Очно-заочно')], default='', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='preview',
            field=models.ImageField(height_field='480', upload_to='courses/%Y/%m/%d/', width_field='854'),
        ),
    ]