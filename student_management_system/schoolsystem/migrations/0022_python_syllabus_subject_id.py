# Generated by Django 4.2.4 on 2023-09-23 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0021_python_syllabus'),
    ]

    operations = [
        migrations.AddField(
            model_name='python_syllabus',
            name='subject_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schoolsystem.subject'),
        ),
    ]
