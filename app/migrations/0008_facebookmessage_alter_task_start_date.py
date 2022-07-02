# Generated by Django 4.0.5 on 2022-07-01 23:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_lesson_options_remove_lesson_student_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200)),
                ('message', models.CharField(max_length=200)),
                ('sender_psid', models.CharField(max_length=50)),
                ('request_data', models.CharField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 2, 1, 52, 46, 612679)),
        ),
    ]