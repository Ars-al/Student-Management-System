# Generated by Django 4.2.4 on 2023-09-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0020_student_result_class_activity_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Python_Syllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('topics', models.TextField()),
            ],
        ),
    ]
