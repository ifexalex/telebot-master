# Generated by Django 4.0.6 on 2022-07-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_telegramusermessage_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramusermessage',
            name='message',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
