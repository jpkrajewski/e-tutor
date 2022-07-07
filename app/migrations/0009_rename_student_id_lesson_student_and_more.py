# Generated by Django 4.0.5 on 2022-07-02 15:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_facebookmessage_alter_task_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='student_id',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='tutor_id',
            new_name='tutor',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='tutor_id',
            new_name='tutor',
        ),
        migrations.RenameField(
            model_name='teachingroom',
            old_name='lesson_id',
            new_name='lesson',
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 2, 17, 43, 42, 494643)),
        ),
    ]
