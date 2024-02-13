# Generated by Django 4.2.4 on 2023-09-05 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0017_attendance_attendance_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_marks', models.IntegerField()),
                ('exam_marks', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolsystem.student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolsystem.subject')),
            ],
        ),
    ]