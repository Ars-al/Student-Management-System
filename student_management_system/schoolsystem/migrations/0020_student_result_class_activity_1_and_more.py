# Generated by Django 4.2.4 on 2023-09-13 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0019_student_result_assignment_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_result',
            name='class_activity_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='class_activity_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='mid_term',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='quiz_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='quiz_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='quiz_3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_result',
            name='quiz_4',
            field=models.IntegerField(default=0),
        ),
    ]
