# Generated by Django 4.2.4 on 2023-10-24 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0037_exampaper'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampaper',
            name='exam_time_end',
            field=models.DateTimeField(null=True),
        ),
    ]