# Generated by Django 4.0.6 on 2022-07-26 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_telegramusermessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramusermessage',
            name='date_added',
        ),
    ]