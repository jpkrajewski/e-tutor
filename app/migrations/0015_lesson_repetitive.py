# Generated by Django 4.0.5 on 2022-08-17 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_delete_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='repetitive',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
