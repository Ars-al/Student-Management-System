# Generated by Django 4.2.4 on 2023-12-19 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsystem', '0049_alter_invoice_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='serial_number',
        ),
    ]