# Generated by Django 4.0.6 on 2022-07-11 20:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_telegramuser_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='message_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), size=100),
        ),
    ]
