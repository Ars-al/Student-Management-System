# Generated by Django 4.2.4 on 2023-09-01 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0012_student_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_feedback',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolsystem.student'),
        ),
    ]