# Generated by Django 4.2.4 on 2023-09-30 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0028_syllabus_notes_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diary_date', models.DateField()),
                ('diary', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolsystem.subject')),
            ],
        ),
    ]
