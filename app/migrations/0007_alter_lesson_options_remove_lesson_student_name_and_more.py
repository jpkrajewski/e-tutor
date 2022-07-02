# Generated by Django 4.0.5 on 2022-07-01 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_student_level_lesson_student_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['lesson_start_datetime']},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='student_name',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 2, 0, 35, 56, 954359)),
        ),
    ]