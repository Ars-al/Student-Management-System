# Generated by Django 4.2.4 on 2023-12-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0046_remove_invoice_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='serial_number',
            field=models.CharField(default='#0000', max_length=20, unique=True),
        ),
    ]
